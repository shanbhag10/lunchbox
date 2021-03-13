import db.user as user_db
from db.user import *

def create_new_user(request):
    user = user_db.User(
        request['first_name'], request['last_name'], request['email'], request['password'],
        request['address'], request['phone_number'], request['chef'], None, None)

    user_db.save_user(user)


def validate_credentials(email, password):
    user = user_db.get_user_by_email(email)
    if (user == None):
        return False
    return user.password == password

def does_user_exist(email):
    user = user_db.get_user_by_email(email)
    return user != None