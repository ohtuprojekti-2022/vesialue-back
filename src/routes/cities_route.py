from flask import request
from flask_restx import Namespace, Resource
import requests as req
from utils.config import BIG_DATA_API_KEY

api = Namespace('cities')

@api.route('')
class GetCity(Resource):
    def get(self):
        args = request.args.to_dict()
        if not args['latitude'] or not args['longitude']:
            return { 'error': 'bad request'}, 400

        params = dict(
            latitude = args['latitude'],
            longitude = args['longitude'],
            localityLanguage = 'fi',
            key = BIG_DATA_API_KEY
        )
        url = 'https://api.bigdatacloud.net/data/reverse-geocode'
        response = req.get(url=url, params=params)
        return response.json(), 200
