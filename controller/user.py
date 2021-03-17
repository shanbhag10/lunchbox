import db.user as user_db
from db.user import *

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