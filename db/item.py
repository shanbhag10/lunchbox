from datetime import datetime
from app import db

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer)
    name = db.Column(db.String(200))
    item_type = db.Column(db.String(200))
    cost = db.Column(db.Integer)
    description = db.Column(db.Text())
    picture_url = db.Column(db.String(200))
    portion_size = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.String(200))
    updated_at = db.Column(db.String(200))

    def __init__(self, name, chef_id, item_type, cost, description, picture_url, portion_size):
        self.name = name
        self.chef_id = chef_id
        self.item_type = item_type
        self.cost = cost
        self.description = description
        self.picture_url = picture_url
        self.portion_size = portion_size
        self.rating = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    pickup_start_time = db.Column(db.String(200))
    pickup_end_time = db.Column(db.String(200))
    max_quantity = db.Column(db.Integer)
    created_at = db.Column(db.String(200))
    updated_at = db.Column(db.String(200))

    def __init__(self, item_id, pickup_start_time, pickup_end_time, max_quantity):
        self.item_id = item_id
        self.pickup_start_time = pickup_start_time
        self.pickup_end_time = pickup_end_time
        self.max_quantity = max_quantity
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

def get_items_by_chef(chef_id):
    return db.session.query(Item).filter(Item.chef_id == chef_id) 

def save_item(item):
    db.session.add(item)
    db.session.commit()

def save_meal(meal):
    db.session.add(meal)
    db.session.commit()