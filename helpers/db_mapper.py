def user_to_dict(user):
    user_profile = {}
    user_profile['First Name'] = user.first_name
    user_profile['Last Name'] = user.last_name
    user_profile['Email'] = user.email
    user_profile['Phone Number'] = user.phone_number
    user_profile['Address'] = user.address
    user_profile['Venmo Id'] = user.venmo_id
    user_profile['Profile Picture'] = user.profile_pic_url
    return user_profile


def items_to_dict(items):
    item_dicts = []
    for item in items:
        item_dict = {}
        item_dict['Id'] = item.id
        item_dict['Name'] = item.name
        item_dict['Item Type'] = item.item_type
        item_dict['Description'] = item.description
        item_dict['Cost'] = item.cost
        item_dict['Portion Size'] = item.portion_size
        item_dict['Picture'] = item.picture_url
        item_dicts.append(item_dict)

    return item_dicts


def meals_by_chef(meals):
    meals_by_chef = {}

    for meal in meals:
        if meal.chef_id not in meals_by_chef:
            meals_by_chef[meal.chef_id] = []
        meals_by_chef[meal.chef_id].append(meal_to_dict(meal))

    return meals_by_chef


def meals_to_dicts(meals):
    meals_dicts = []
    for meal in meals:
        meals_dicts.append(meal_to_dict(meal))
    return meals_dicts


def meal_to_dict(meal):
    meal_dict = {}
    meal_dict['Id'] = meal.id
    meal_dict['Date'] = meal.date
    meal_dict['Chef Id'] = meal.chef_id
    meal_dict['Pickup Start Time'] = meal.pickup_start_time.strftime("%I:%M %p")
    meal_dict['Pickup End Time'] = meal.pickup_end_time.strftime("%I:%M %p")
    meal_dict['Items'] = items_to_dict(meal.items)
    return meal_dict
