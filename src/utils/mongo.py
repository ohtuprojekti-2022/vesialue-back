from pymodm.connection import connect
from src.utils.config import MONGO_URI


def connect_to_db():
    connect(MONGO_URI, alias='app')
