import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://postgres:admin123@localhost:5433/logindb') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
        #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:admin123@localhost:5433/logindb')
