from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    venmo_id = db.Column(db.String(200))
    address = db.Column(db.String(400))
    phone_number = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    user_type = db.Column(db.String(200))
    about = db.Column(db.Text())
    created_at = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, password, address, phone_number, user_type, venmo_id, about):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.address = address
        self.phone_number = phone_number

        self.rating = 0
        self.created_at = datetime.now()

        if user_type == 'yes':
            self.user_type = 'chef'
        else:
            self.user_type = 'foodie'

        self.about = about
        self.venmo_id = venmo_id

def get_user_by_email(email):
    users = db.session.query(User).filter(User.email == email)
    if users.count() == 0:
        return None
    return users.first()

def save_user(user):
    db.session.add(user)
    db.session.commit()