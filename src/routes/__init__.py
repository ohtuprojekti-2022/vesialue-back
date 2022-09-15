from flask_restx import Api

from .inventory_route import api as add_inventory_api

api=Api(
    title='Api for Vesialueen inventointi-ilmoitus'
)

api.add_namespace(add_inventory_api, path='/api/add_inventory')
