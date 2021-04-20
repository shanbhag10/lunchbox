from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, index=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    venmo_id = db.Column(db.String(200))
    address = db.Column(db.String(400))
    phone_number = db.Column(db.String(200))
    profile_pic_url = db.Column(db.String(600))
    user_type = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, password, address, phone_number, user_type, venmo_id, about):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.address = address
        self.phone_number = phone_number
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.venmo_id = venmo_id
        self.rating = 0

        if user_type == 'yes':
            self.user_type = 'chef'
        else:
            self.user_type = 'foodie'


class Chef(db.Model):
    __tablename__ = 'chefs'
    user_id = db.Column(db.Integer, unique=True, primary_key=True)
    rating = db.Column(db.Integer)
    about = db.Column(db.Text())
    speciality = db.Column(db.String(200))

    def __init__(self, user_id, rating, about, speciality):
        self.user_id = user_id
        self.rating = 0
        self.about = about
        self.speciality = speciality


def get_user_by_email(email):
    users = db.session.query(User).filter(User.email == email)
    if users.count() == 0:
        return None
    return users.first()


def get_user_by_id(user_id):
    users = db.session.query(User).filter(User.id == user_id)
    if users.count() == 0:
        return None
    return users.first()


def get_users_by_ids(user_ids):
    return db.session.query(User).filter(User.id.in_(user_ids))
    

def save_user(user):
    db.session.add(user)
    db.session.commit()


def update_user():
    db.session.commit()


def save_chef(chef):
    db.session.add(chef)
    db.session.commit()