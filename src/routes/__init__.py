from flask_restx import Api

from .register import api as register_api

api=Api(
    title='Api for Vesialueen inventointi-ilmoitus'
)

api.add_namespace(register_api, path='/api/register')

