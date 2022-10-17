from flask_restx import Api
from .inventory_route import api as inventory_api
from .register import api as register_api
from .login import api as login_api
from .cities import api as cities_api

api=Api(
    title='Api for Vesialueen inventointi-ilmoitus'
)

api.add_namespace(register_api, path='/api/register')
api.add_namespace(login_api, path='/api/login')
api.add_namespace(inventory_api, path='/api/inventory')
api.add_namespace(cities_api, path='/api/cities')