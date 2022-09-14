from flask import Flask
from models.user import User
from utils.mongo import connect_to_db

connect_to_db()

app = Flask(__name__)

@app.route("/")
def index():
    User.create("abaa", "aaaaaaaaaa", "aaa", "aaa", "aaa")
    return "Hello world!"