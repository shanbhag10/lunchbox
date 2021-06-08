import db.item as item_db
from db.item import *
import datetime


def create_new_item(request, chef_id, pic_url):
    item = item_db.Item(
        request['item_name'], chef_id, request['item_type'], request['cost'],
        request['description'], pic_url, request['portion_size'])

    item_db.save_item(item)


def get_items_for_chef(chef_id):
    return item_db.get_items_by_chef(chef_id)


def add_new_meal(request, user_id):
    meal = item_db.Meal(request['meal_date'], 
        user_id, request['pickup_time'])

    items = get_items_for_chef(user_id)
    for item in items:
        if 'item_' + str(item.id) in request:
            meal.items.append(item)

    item_db.save_meal(meal)


def get_meals_for_chef(chef_id):
    return item_db.get_meals_by_chef(chef_id)


def get_upcoming_meals():
    return item_db.get_upcoming_meals()


def get_items_by_ids(ids):
    return item_db.get_items_by_ids(ids)