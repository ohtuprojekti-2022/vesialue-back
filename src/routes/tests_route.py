from flask_restx import Namespace, Resource
from tests import test_tools as tools

api = Namespace('tests')


@api.route('/reset')
class Tests(Resource):
    def post(self):
        try:
            tools.delete_all_users()
            tools.delete_all_inventories()
            tools.delete_all_edited_inventories()
        except Exception as e:
            return {f'{type(e)}': e.args}, 400
        return 'Reset succeed', 200
