from flask import Flask, request
from flask_restful import reqparse, Resource, Api
from json import dumps

from elevation.cmds.predict import Predict

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('wildtype', type=str, action='append')
parser.add_argument('offtarget', type=str, action='append')

predictor = Predict()

class ElevationPrediction(Resource):
    def post(self):
        args = parser.parse_args()

        wt = args['wildtype']
        mut = args['offtarget']

        # The Predict.execute() numpy arrays aren't JSON serializable, so convert to list.
        prediction = predictor.execute(wt, mut)
        return {score: prediction[score].tolist() for score in prediction}

api.add_resource(ElevationPrediction, '/elevation')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
