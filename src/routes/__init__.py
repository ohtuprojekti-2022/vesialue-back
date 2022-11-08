# import os
from flask_restx import Api
from .inventory_route import api as inventory_api
from .register_route import api as register_api
from .login_route import api as login_api
from .user_route import api as user_api

api = Api(
    title='Api for Vesialueen inventointi-ilmoitus'
)

api.add_namespace(register_api, path='/api/register')
api.add_namespace(login_api, path='/api/login')
api.add_namespace(inventory_api, path='/api/inventory')
api.add_namespace(user_api, path='/api/user')

# if os.getenv('FLASK_ENV') == 'development':
#     api.add_namespace(tests_api, path='/api/tests')
