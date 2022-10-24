import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('FLASK_ENV')
MONGO_URI = os.getenv('TEST_MONGO_URI') if ENV == 'test' else os.getenv('MONGO_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
BIG_DATA_API_KEY = os.getenv('BIG_DATA_API_KEY')
