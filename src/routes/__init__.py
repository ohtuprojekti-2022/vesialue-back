from flask_restx import Api
from .inventory_route import api as add_inventory_api
from .register import api as register_api
from .login import api as login_api

api=Api(
    title='Api for Vesialueen inventointi-ilmoitus'
)

api.add_namespace(register_api, path='/api/register')
api.add_namespace(login_api, path='/api/login')
api.add_namespace(add_inventory_api, path='/api/add_inventory')
