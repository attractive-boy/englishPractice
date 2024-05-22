# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    USERNAME = os.getenv('DATABASE_USERNAME', 'root')
    PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    HOST = os.getenv('DATABASE_HOST', 'localhost')
    DB_NAME = os.getenv('DATABASE_NAME', 'english_practice')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SESSION_TYPE = 'filesystem'

