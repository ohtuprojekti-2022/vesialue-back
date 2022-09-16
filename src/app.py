from flask import Flask
from utils.mongo import connect_to_db
from routes import api
from utils.config import SECRET_KEY

connect_to_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

api.init_app(app)