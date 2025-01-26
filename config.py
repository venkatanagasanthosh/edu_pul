import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://postgres:admin123@localhost:5433/logindb') or 'postgresql://postgres:admin123@localhost:5433/logindb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
