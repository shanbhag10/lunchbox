import db.order as order_db
from db.order import *
from controller.item import *
import datetime

def place_new_order(request, user_id):
    notes = ''
    meal_id = ''
    chef_id = ''
    for key, value in request.items():
        if 'notes' in key:
            ids = key.split('_')
            notes = value
            meal_id = ids[0]
            chef_id = ids[1]

    order = order_db.Order(
        user_id, meal_id, chef_id, notes, request['pickup_time_in'])

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
    for item in items.values():
        if item.id in item_qty_dict:
            total_cost += item.cost * item_qty_dict[item.id]
    order.total_cost = total_cost
    order_db.save_order(order)


def get_orders_for_user(user_id):
    return order_db.get_orders_for_user(user_id)


def get_orders_for_chef(chef_id):
    return order_db.get_orders_for_chef(chef_id)
