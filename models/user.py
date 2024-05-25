from sqlalchemy.sql import func
from flask_login import UserMixin
from db.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, email, username, password, first_name, last_name):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def get_id(self):
        return str(self.id)

