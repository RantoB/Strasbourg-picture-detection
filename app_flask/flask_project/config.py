import json

with open('/home/ranto/.config/config_flask_app.json') as f:
    config = json.load(f)

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
