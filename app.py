from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import os

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

if os.environ.get('STAGE') != 'prod':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LionelMessi10@localhost/lunchbox'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
Session(app)

from db.user import *
from db.item import *
from db.order import *
from controller.user import *
from controller.item import *
from controller.order import *
from helpers.validator import *
from helpers.db_mapper import *
from helpers.s3 import *


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        try:
            if not validate_create_request(request.form):
                return render_template('create_account.html', message='Please enter all required fields correctly')
            
            if does_user_exist(request.form['email']):
                return render_template('create_account.html', message='User with this email already exists. Try logging in.')
            
            create_new_user(request.form)
            return render_template('login.html', message='Successfully created your account. Welcome to lunchbox. :D Please sign in')
        except Exception as e:
            print("Account creation error : " + str(e))
            return render_template('login.html', message='Something went wrong. Please try again')
    
    return render_template('create_account.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            if email == '' or password == '':
                return render_template('login.html', message='Please enter required fields')

            if not validate_credentials(email, password):
                return render_template('login.html', message='Email or password incorrect. Please try again')

            session['email'] = email
            user = get_user_by_email(session['email'])
            session['user_id'] = user.id
            session['date'] = datetime.today

            return redirect(url_for('home', page='meals'))
        except Exception as e:
            print("Login error : " + str(e))

    return render_template('login.html', message='Something went wrong. Please try again')


@app.route('/home/<page>', methods=['GET'])
def home(page):
    user = None
    try:
        user = get_user_by_email(session['email']) 
    except Exception as e:
        print("Session error : " + str(e))
        return render_template('login.html', message='Session timed out. Please login again')

    try:
        user_profile = user_to_dict(user)

        if user.user_type == 'chef':
            items = get_items_for_chef(session['user_id'])
            items_dicts = items_to_dict(items)

            meals = get_meals_for_chef(session['user_id'])
            meals_dicts = meals_to_dicts(meals)

            users_for_orders = {}
            orders_dicts = {}
            orders = get_orders_for_chef(session['user_id'])
            if orders != None:
                for order in orders:
                    users_for_orders[order.id] = get_user_by_id(order.user_id)

                orders_dicts = orders_to_dicts(orders, users_for_orders)

            return render_template('chef_home.html', user_profile=user_profile, items_dicts=items_dicts, meals_dicts=meals_dicts, page=page, orders_dicts=orders_dicts)
        
        meals = get_upcoming_meals()
        meals_dicts = meals_by_chef(meals)
        orders = get_orders_for_user(session['user_id'])
        
        chefs = []
        orders_dicts = {}
        if orders != None:
            chefs_for_orders = {}
            for order in orders:
                chefs_for_orders[order.id] = get_user_by_id(order.chef_id)

            orders_dicts = orders_to_dicts(orders, chefs_for_orders)

        chefs = get_users_by_ids(meals_dicts.keys())

        return render_template('user_home.html', user_profile=user_profile, meals_dicts=meals_dicts, chefs=chefs, page=page, orders_dicts=orders_dicts)

    except Exception as e:
        print("Homepage failure : " + str(e))
        return render_template('login.html', message='Could not load home page. Please login again')


@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        try:
            pic_url = upload_pic(request.files['item_picture'], session['user_id'], request.form['item_name'])
            create_new_item(request.form, session['user_id'], pic_url)
            return redirect(url_for('home', page='items', message='Successfully added item'))
        except Exception as e:
            print("Add item failed : " + str(e))
            return redirect(url_for('home', page='items', message='Failed to add item. Please try again'))


@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
    if request.method == 'POST':
        try:
            pic_url = upload_pic(request.files['profile_pic'], session['user_id'], request.form['first_name_in'])
            update_user_profile(request.form, session['user_id'], pic_url)
            return redirect(url_for('home', page='profile', message='Successfully updated profile'))
        except Exception as e:
            print("Update profile failed : " + str(e))
            return redirect(url_for('home', page='profile', message='Failed to updated profile. Please try again'))


@app.route('/add_meal', methods=['POST', 'GET'])
def add_meal():
    if request.method == 'POST':
        try:
            add_new_meal(request.form, session['user_id'])
            return redirect(url_for('home', page='meals', message='Successfully added meal'))
        except Exception as e:
            print("Add meal failed : " + str(e))
            return redirect(url_for('home', page='meals', message='Failed to add meal. Please try again'))


@app.route('/delete_meal/<meal_id>', methods=['POST', 'GET'])
def delete_meal(meal_id):
    if request.method == 'POST':
        try:
            delete_meal_by_id(meal_id)
            return redirect(url_for('home', page='meals', message='Successfully deleted meal'))
        except Exception as e:
            print("Delete meal failed : " + str(e))
            return redirect(url_for('home', page='meals', message='Failed to delete meal. Please try again'))

    return redirect(url_for('home', page='meals', message='Failed to delete meal. Please try again'))


@app.route('/place_order/<meal_id>/<chef_id>/<date>', methods=['POST', 'GET'])
def place_order(meal_id, chef_id, date):
    if request.method == 'POST':
        try:
            place_new_order(request.form, session['user_id'], meal_id, chef_id, date)
            return redirect(url_for('home', page='orders', message='Order placed successfully. Track it in the Orders tab.'))
        except Exception as e:
            print("Order placement failed : " + str(e))
            return redirect(url_for('home', page='orders', message='Failed to place order. Please try again'))


@app.route('/update/<order_id>/<status>', methods=['POST', 'GET'])
def update_order(order_id, status):
    if request.method == 'POST':
        try:
            update_order_status(order_id, status)
            return redirect(url_for('home', page='orders', message='Order updated successfully.'))
        except Exception as e:
            print("Order update failed : " + str(e))
            return redirect(url_for('home', page='orders', message='Failed to update order. Please try again'))


if __name__ == '__main__':
    app.run(debug=True)