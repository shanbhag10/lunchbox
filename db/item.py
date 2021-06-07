from datetime import datetime, date
from app import db
from sqlalchemy.orm import relationship, backref

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer)
    name = db.Column(db.String(200), unique=True, index=True)
    item_type = db.Column(db.String(200))
    cost = db.Column(db.Float)
    description = db.Column(db.Text())
    picture_url = db.Column(db.String(600))
    portion_size = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    date = db.Column(db.Date)
    chef_id = db.Column(db.Integer)
    pickup_start_time = db.Column(db.Time)
    pickup_end_time = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = relationship("Item", secondary="items_meals_association")

    def __init__(self, date, chef_id, pickup_start_time, pickup_end_time):
        self.date = date
        self.chef_id = chef_id
        self.pickup_start_time = pickup_start_time
        self.pickup_end_time = pickup_end_time
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class Items_meals_association(db.Model):
    __tablename__ = 'items_meals_association'
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    max_qty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    item = relationship(Item, backref=backref("items_meals_association", cascade="all, delete-orphan"))
    meal = relationship(Meal, backref=backref("items_meals_association", cascade="all, delete-orphan"))

    def __init__(self, meal_id, item_id, max_qty):
        self.item_id = item_id
        self.meal_id = meal_id
        self.max_qty = max_qty
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


def get_items_by_chef(chef_id):
    return db.session.query(Item).filter(Item.chef_id == chef_id) 


def get_meals_by_chef(chef_id):
    return db.session.query(Meal).filter(Meal.chef_id == chef_id).filter(Meal.date >= date.today())


def get_upcoming_meals():
    return db.session.query(Meal).filter(Meal.date >= date.today())


def save_item(item):
    db.session.add(item)
    db.session.commit()


def save_meal(meal):
    db.session.add(meal)
    db.session.commit()