import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('FLASK_ENV') or 'production'
E2E_ENV = os.getenv('E2E_ENV')

if E2E_ENV or ENV == 'test':
    MONGO_URI = os.getenv('TEST_MONGO_URI')
else:
    MONGO_URI = os.getenv('MONGO_URI')

SECRET_KEY = os.getenv('SECRET_KEY')
BIG_DATA_API_KEY = os.getenv('BIG_DATA_API_KEY')
