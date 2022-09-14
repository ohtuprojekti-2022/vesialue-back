from flask import Flask
from models.user import User
from utils.mongo import connect_to_db
from routes import api

connect_to_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaaaaaaaa'

api.init_app(app)

#@app.route("/")
#def index():
#    User.create("abaa", "aaaaaaaaaa", "aaa", "aaa", "aaa")
#    return "Hello world!"