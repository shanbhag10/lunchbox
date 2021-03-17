import db.item as item_db
from db.item import *

def create_new_item(request, chef_id, pic_url):
    item = item_db.Item(
        request['item_name'], chef_id, request['item_type'], request['cost'],
        request['description'], pic_url, request['portion_size'])

    item_db.save_item(item)

def get_items_for_chef(chef_id):
    return item_db.get_items_by_chef(chef_id)