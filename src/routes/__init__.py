from flask_restx import Api
from utils.config import ENV, E2E_ENV
from .inventory_route import api as inventory_api
from .register_route import api as register_api
from .login_route import api as login_api
from .user_route import api as user_api
from .tests_route import api as tests_api
from .upload_route import api as upload_api

api = Api(
    title='Api for Vesialueen inventointi-ilmoitus'
)

api.add_namespace(register_api, path='/api/register')
api.add_namespace(login_api, path='/api/login')
api.add_namespace(inventory_api, path='/api/inventory')
api.add_namespace(user_api, path='/api/user')
api.add_namespace(upload_api, path='/api/upload')

if E2E_ENV or ENV == 'development':
    api.add_namespace(tests_api, path='/api/tests')
