import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
BIG_DATA_API_KEY = os.getenv('BIG_DATA_API_KEY')
