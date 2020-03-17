# Elevation

Off-target effects of the CRISPR-Cas9 system can lead to suboptimal gene
editing outcomes and are a bottleneck in its development. Here, we introduce
two interdependent machine learning models for the prediction of off-target
effects of CRISPR-Cas9. The approach, which we named Elevation, scores
individual guide–target pairs, and aggregates such scores into a single,
overall summary guide score.

See our [**official project page**](https://www.microsoft.com/en-us/research/project/crispr/) for more detail.

## Publications

Please cite this paper if using our predictive model:

Jennifer Listgarten\*, Michael Weinstein\*, Benjamin P. Kleinstiver,
Alexander A. Sousa, J. Keith Joung, Jake Crawford, Kevin Gao, Luong Hoang,
Melih Elibol, John G. Doench\*, Nicolo Fusi\*. [**Prediction of off-target
activities for the end-to-end design of CRISPR guide RNAs.**](https://doi.org/10.1038/s41551-017-0178-6)
*Nature Biomedical Engineering*, 2018.

(\* = equal contributions/corresponding authors)

## Dependencies

### Install Python and dependencies

1. Install Python 2.7

Latest Python 2.7.x is acceptable, the example below uses `2.7.16`.

On Windows, use [`pyenv-win`](https://github.com/pyenv-win/pyenv-win).
On Unix and macOS, use [`pyenv`](https://github.com/pyenv/pyenv).

```
  pyenv install 2.7.16
```

2. Activate Python in the shell, install `virtualenv` and create a virtual
   environment.  Branches other than `master` may use Python 3, so it is helpful
   to name the virtual environment according to the python version.

```
  pyenv local 2.7.16
  pip install --upgrade pip # Optional
  pip install virtualenv
  virtualenv 2
  source 2/bin/activate
```

3. Install the dependencies.

```
  pip install -r requirements.txt
```

### Install data dependencies

1. Follow the instructions in the [`elevation-data`](https://github.com/richardkmichael/elevation-data) repository.

Afterward, the directory structure should look like:

```
elevation/
    CRISPR/
        data/
            offtarget/
                Haeussler/
                CD33_data_postfilter.xlsx
                nbt.3117-S2.xlsx
                STable 18 CD33_OffTargetdata.xlsx
                STable 19 FractionActive_dlfc_lookup.xlsx
                Supplementary Table 10.xlsx
        gene_sequences/
            CD33_sequence.txt
        guideseq/
            guideseq.py
            guideseq_unique.txt
            guideseq_unique_MM6_end0_lim999999999.hdf5
    cache/
    CHANGELOG.md
    elevation/
    ...
```

2. Decompress the pickled prepared data and models, these are used if not re-training a model.

```
  xz -kd tmp/*.pkl.xz
```

### Test installation

Make sure everything is set up properly by running the following command from
the root directory of the repository.  If a test fails, running again with `-s` can
be helpful to see the output.

```
  python -m pytest tests
```

## Use

The following example code is available in a [Jupyter notebook](/notebooks/README_Example.ipynb).

The Jupyter notebook is not at the top-level directory with Elevation, so the `PYTHONPATH` will need
to be adjusted for the Elevation modules to import.  Adjusting the `PYTHONPATH` can be done on the
command line, as below; or in the notebook itself by adding to `sys.path`.

```
  pip install jupyter
  PYTHONPATH=.. jupyter notebook notebooks
```

### Guide Sequence Prediction

```python
import elevation.load_data
from elevation.cmds.predict import Predict

# load data
num_x = 100
roc_data, roc_Y_bin, roc_Y_vals = elevation.load_data.load_HauesslerFig2(1)
wildtype = list(roc_data['30mer'])[:num_x]
offtarget = list(roc_data['30mer_mut'])[:num_x]

# initialize predictor
p = Predict()

# run prediction
preds = p.execute(wildtype, offtarget)

# preds is a dictionary of the form {'linear-raw-stacker': [...], 'CFD': [...]}
for i in range(num_x):
    print(wildtype[i], offtarget[i], map(lambda kv: kv[0] + "=" + str(kv[1][i]), preds.iteritems()))
```

### Aggregation Prediction

```python
import numpy as np
import pickle
import elevation.load_data
from elevation.cmds.predict import Predict
from elevation import settings
from elevation import aggregation

# load data
num_x = 100
roc_data, roc_Y_bin, roc_Y_vals = elevation.load_data.load_HauesslerFig2()
wildtype = list(roc_data['30mer'])[:num_x]
offtarget = list(roc_data['30mer_mut'])[:num_x]

# initialize guide seq predictor
p = Predict()

# run prediction
preds = p.execute(wildtype, offtarget)

# load aggregation model
with open(settings.agg_model_file) as fh:
    final_model, other = pickle.load(fh)

# compute aggregated score
isgenic = np.zeros(num_x, dtype=np.bool)
result = aggregation.get_aggregated_score(
         preds['linear-raw-stacker'],
         preds['CFD'],
         isgenic,
         final_model)
print result
```

### Recomputing Models

Models are persisted as pickle files and, under certain circumstances,
may need to be recomputed. Elevation models depend on the CRISPR repository.
To recompute models, run the following command.

```
  elevation-fit --crispr_repo_dir /path/to/elevation/CRISPR
```

### New Fixtures

After making changes to the models, to generate new fixtures (data used to test
prediction consistency), run `elevation-fixtures`.

Run `python -m pytest tests` to make sure tests are still passing.

### Settings

If you'd like to reconfigure the default location of CRISPR, the temp dir in
which pickles are stored, etc., copy `elevation/settings_template.py` to
`elevation/settings.py` and edit `elevation/settings.py` before installation.

If `elevation/settings.py` does not exist at install time, then
`elevation/settings_template.py` is used to create `elevation/settings.py`.

## Contacting us

You can submit bug reports using the GitHub issue tracker. If you have any
other questions, please contact us at crispr@lists.research.microsoft.com.
