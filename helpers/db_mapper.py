def user_to_dict(user):
    user_profile = {}
    user_profile['Email'] = user.email
    user_profile['Id'] = user.id
    user_profile['First Name'] = user.first_name
    user_profile['Last Name'] = user.last_name
    return user_profile