from flask import Flask
from utils import mongo, config
from routes import api

mongo.connect_to_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

api.init_app(app)
