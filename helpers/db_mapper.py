def user_to_dict(user):
    user_profile = {}
    user_profile['Email'] = user.email
    user_profile['First Name'] = user.first_name
    user_profile['Last Name'] = user.last_name
    user_profile['Phone Number'] = user.phone_number
    user_profile['Address'] = user.address
    user_profile['Venmo Id'] = user.venmo_id
    user_profile['Profile Picture'] = user.profile_pic_url
    return user_profile

def items_to_dict(items):
    item_dicts = []
    for item in items:
        item_dict = {}
        item_dict['Name'] = item.name
        item_dict['Item Type'] = item.item_type
        item_dict['Description'] = item.description
        item_dict['Cost'] = item.cost
        item_dict['Portion Size'] = item.portion_size
        item_dict['Picture'] = item.picture_url
        item_dicts.append(item_dict)

    return item_dicts

