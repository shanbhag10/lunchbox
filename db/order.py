from datetime import datetime
from app import db
from sqlalchemy.orm import relationship, backref
from db.item import *


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    meal_id = db.Column(db.Integer)
    chef_id = db.Column(db.Integer)
    status = db.Column(db.String(200))
    notes = db.Column(db.String(400))
    total_cost = db.Column(db.Float)
    pickup_time = db.Column(db.Time)
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = relationship("Order_item")

    def __init__(self, user_id, meal_id, chef_id, notes, date):
        self.user_id = user_id
        self.meal_id = meal_id
        self.chef_id = chef_id
        self.status = "Placed"
        self.notes = notes
        self.date = date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class Order_item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    rating = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    item = relationship(Item, backref=backref("order_items", cascade="all, delete-orphan"))

    def __init__(self, order_id, item_id, qty):
        self.order_id = order_id
        self.item_id = item_id
        self.qty = qty
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.rating = 0


def get_orders_for_user(user_id):
    orders = db.session.query(Order).filter(Order.user_id == user_id)
    if orders.count() == 0:
        return None
    return orders


def get_orders_for_chef(chef_id):
    orders = db.session.query(Order).filter(Order.chef_id == chef_id)
    if orders.count() == 0:
        return None
    return orders


def get_order_by_id(order_id):
    orders = db.session.query(Order).filter(Order.id == order_id)
    if orders.count() == 0:
        return None
    return orders.first()
    

def save_order(order):
    db.session.add(order)
    db.session.commit()


def update_order():
    db.session.commit()