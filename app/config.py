import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
    AUTH_URI = os.environ.get('GOOGLE_AUTH_URI')
    TOKEN_URI = os.environ.get('GOOGLE_TOKEN_URI')
    USER_INFO = os.environ.get('GOOGLE_USER_INFO_URI')
    SCOPE = ['openid', 'email', 'profile']