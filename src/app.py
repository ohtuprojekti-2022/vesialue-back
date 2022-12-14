from flask import Flask
from flask_cors import CORS
from utils import mongo, config
from routes import api

mongo.connect_to_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['ERROR_404_HELP'] = False
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 # max file upload size

CORS(app)

api.init_app(app)
