import db.order as order_db
from db.order import *
from controller.item import *
from controller.user import *
from helpers.email import *
import datetime

def place_new_order(request, user_id, meal_id, chef_id, date):
    order = order_db.Order(user_id, meal_id, chef_id, request['notes_in'], date)

    order_items = []
    item_qty_dict = {}
    for key, value in request.items():
        if 'qty' in key and value != '': 
            qty = int(value)         
            item_id = int(key.split('_')[0])
            
            order_item = order_db.Order_item(
                order.id, item_id, qty)
            
            order_items.append(order_item)
            item_qty_dict[item_id] = qty

    order.order_items = order_items
    items = get_items_by_ids([*item_qty_dict])

    total_cost = 0
    for item in items:
        if item.id in item_qty_dict:
            total_cost += item.cost * item_qty_dict[item.id]
    order.total_cost = total_cost
    order_db.save_order(order)


def get_orders_for_user(user_id):
    return order_db.get_orders_for_user(user_id)


def get_orders_for_chef(chef_id):
    return order_db.get_orders_for_chef(chef_id)


def update_order_status(order_id, status):
    order = order_db.get_order_by_id(order_id)
    order.status = status
    if status == 'Ready':
        user = get_user_by_id(order.user_id)
        chef = get_user_by_id(order.chef_id)
        body = build_order_ready_email(order, user, chef)
        send_email(user.email, "Your order is ready!", body)
    return order_db.update_order()
