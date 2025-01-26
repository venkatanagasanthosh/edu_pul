import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:admin123@localhost:5433/logindb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    # Removed Twilio configurations
    # TWILIO_ACCOUNT_SID = 'VA9b7ad6f8401959ce485a4bab7e312044'
    # TWILIO_AUTH_TOKEN = '09677ce94dd0fa3db7a43af941baffd9'
    # TWILIO_PHONE_NUMBER = '+919010902836'