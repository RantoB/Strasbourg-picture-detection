from flask_project import db
from flask import current_app
from flask_login import UserMixin
# This provides default implementations
# for the methods that Flask-Login expects user objects to have.

class User(db.Model, UserMixin):    
    pass
