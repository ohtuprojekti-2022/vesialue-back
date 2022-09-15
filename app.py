from flask import Flask
from src.models.inventory import Inventory
from src.utils.mongo import connect_to_db
from src.routes import api

connect_to_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

api.init_app(app)
