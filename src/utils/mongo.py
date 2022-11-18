from pymodm.connection import connect, _get_db
from utils.config import MONGO_URI


def connect_to_db():
    connect(MONGO_URI, alias='app')

def get_database():
    return _get_db(alias='app')
