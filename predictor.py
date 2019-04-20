# -*- coding: UTF-8 -*-

# Usage:
#   cat guides-genes.json | python predictor.py > predictions.json

import numpy
import pickle
import json
import sys

import elevation.load_data
from elevation.cmds.predict import Predict
from elevation import settings
from elevation import aggregation

# Load Hauessler version 1, which means data comes from the TAB file:
#   Haeussler/fig2-crisporData_withReadFraction.tab

# The TAB file data is asserted to be sequences for length 23, then filtered to be only off-target
# sequences (30mer_mut) ending in AG and GG with a readFraction sum .allclose() to
# 6.6659440001416188 Finally, the returned data has been annotated;
# see load_data.py:annot_from_seqs().
#
# However, none of this extra information is actually used.
#
#
# Returns:
#   roc_data:   DataFrame [30mer, 30mer_mut, wasValidated, readFraction]
#   roc_Y_bin:  data[wasValidated]
#   roc_Y_vals: data[readFraction]

# Receiver Operating Charateristic (area under curve)
# https://en.wikipedia.org/wiki/Receiver_operating_characteristic

# FIXME: roc_Y_bin, roc_Y_vals are never used, why?
# roc_data, roc_Y_bin, roc_Y_vals = elevation.load_data.load_HauesslerFig2(1)
roc_data = elevation.load_data.load_HauesslerFig2(1)[0]

# load data
# num_x = 100
# wildTypes = list(roc_data['30mer'])[:num_x]
# offTargets = list(roc_data['30mer_mut'])[:num_x]

data = sys.stdin.read()
items = json.loads(data)
num_x = len(items)
wildTypes = [ item['wildType'] for item in items ]
offTargets = [ item['offTarget'] for item in items ]

# initialize predictor, will default to loading the pickled model and data
p = Predict()

# run prediction on the 100 wildtypes and offtargets
preds = p.execute(wildTypes, offTargets)

# A result dictionary, will be serialized to JSON.
result = dict(predictions=[], aggregate=None)

# FIXME:
#
# How does the preds return value from p.execute() have the CFD scores?
#
# The loaded Hauessler data from the TAB file has a column `cfdScore`, but the
# entire dataset is not passed in to the predictor, so somehow the predictor is
# accessing shared data loaded into Elevation itself.  In which case, there is
# no need to extract the 30mer and 30mer_mut arrays, just to pass them back into
# the predictor.. the column names could just be passed to the predictor.

# preds is a dictionary of the form {'linear-raw-stacker': [...], 'CFD': [...]}
for i in range(num_x):
    cfdScore = preds.get('CFD')[i][0]
    linear_raw_stacker = preds.get('linear-raw-stacker')[i]

    result['predictions'].append({'wildType': wildTypes[i],
                                  'offTarget': offTargets[i],
                                  'cfdScore': cfdScore,
                                  'linearRawStacker': linear_raw_stacker})

# load aggregation model
with open(settings.agg_model_file) as fh:
    final_model, other = pickle.load(fh)

# compute aggregated score
isgenic = numpy.zeros(num_x, dtype=numpy.bool)

# FIXME: Returns a single element array, direct access on the return. :-(
result['aggregate'] = aggregation.get_aggregated_score(preds.get('linear-raw-stacker'),
                                                       preds.get('CFD'),
                                                       isgenic,
                                                       final_model)[0]

# with open('predictions.json', 'w') as file:
#    file.write(json.dumps(result))

sys.stdout.write(json.dumps(result))
