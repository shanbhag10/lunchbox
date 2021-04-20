import db.user as user_db
from db.user import *
from helpers.db_mapper import *

def create_new_user(request):
    user = user_db.User(
        request['first_name'], request['last_name'], request['email'], request['password'],
        request['address'], request['phone_number'], request['chef'], None, None)

    user_db.save_user(user)

    if (request['chef'] == 'yes'):
        user_id = get_user_by_email(request['email']).id
        create_new_chef_user(user_id)


def create_new_chef_user(user_id):
    chef = user_db.Chef(user_id, None, None, None)
    user_db.save_chef(chef)


def validate_credentials(email, password):
    user = user_db.get_user_by_email(email)
    if (user == None):
        return False
    return user.password == password


def does_user_exist(email):
    user = get_user_by_email(email)
    return user != None


def get_user_by_email(email):
    return user_db.get_user_by_email(email)


def get_user_by_id(user_id):
    return user_db.get_user_by_id(user_id)


def get_users_by_ids(user_ids):
    users = user_db.get_users_by_ids(user_ids)
    users_by_ids = {}
    for user in users:
        users_by_ids[user.id] = user_to_dict(user)
    return users_by_ids


def update_user(request, user_id, pic_url):
    user = user_db.get_user_by_id(user_id)

    if request['first_name_in'] != '' and request['first_name_in'] != user.first_name :
        user.first_name = request['first_name_in']

    if request['last_name_in'] != '' and request['last_name_in'] != user.last_name :
        user.last_name = request['last_name_in']

    if request['address_in'] != '' and request['address_in'] != user.first_name :
        user.address = request['address_in']

    if request['phone_number_in'] != '' and request['phone_number_in'] != user.phone_number :
        user.phone_number = request['phone_number_in']

    if request['venmo_id_in'] != '' and request['venmo_id_in'] != user.venmo_id :
        user.venmo_id = request['venmo_id_in']

    if pic_url != '' and pic_url != user.profile_pic_url :
        user.profile_pic_url = pic_url

    user_db.update_user()