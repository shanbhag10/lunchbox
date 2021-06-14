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
    meal_dict['Date'] = meal.date.strftime("%m-%d-%Y") if meal.date != None else None
    meal_dict['Chef Id'] = meal.chef_id
    meal_dict['Pickup Time'] = meal.pickup_time.strftime("%I:%M %p") if meal.pickup_time else meal.created_at.strftime("%I:%M %p")
    meal_dict['Items'] = items_to_dict(meal.items)
    return meal_dict


def orders_to_dicts(orders, users):
    orders_dicts = {}
    for order in orders:
        if order.status not in orders_dicts:
            orders_dicts[order.status] = []
        orders_dicts[order.status].append(order_to_dict(order, users[order.id]))

    return orders_dicts


def order_to_dict(order, user):
    order_dict = {}
    order_dict['Id'] = order.id
    if user.user_type == 'chef':
        order_dict['Chef'] = user_to_dict(user)
    else:
        order_dict['User'] = user_to_dict(user)
    order_dict['Meal Id'] = order.meal_id
    order_dict['Status'] = order.status
    order_dict['Notes'] = order.notes
    order_dict['Pickup Time'] = order.pickup_time
    order_dict['Date'] = order.date.strftime("%m-%d-%Y") if order.date != None else None
    order_dict['Created At'] = order.created_at
    order_dict['Total Cost'] = "$" + str(round(order.total_cost, 2))
    order_dict['Order Items'] = order_items_to_dict(order.order_items)
    return order_dict


def order_items_to_dict(order_items):
    order_items_dicts = []
    for order_item in order_items:
        order_items_dict = {}
        order_items_dict['Id'] = order_item.id
        order_items_dict['Item Name'] = order_item.item.name
        order_items_dict['Rating'] = order_item.rating
        order_items_dict['Quantity'] = order_item.qty
        order_items_dicts.append(order_items_dict)

    return order_items_dicts