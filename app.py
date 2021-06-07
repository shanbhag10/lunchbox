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
        if not validate_create_request(request.form):
            return render_template('create_account.html', message='Please enter all required fields correctly')
        
        if does_user_exist(request.form['email']):
            return render_template('create_account.html', message='User with this email already exists. Try logging in.')
        
        create_new_user(request.form)
        return render_template('login.html', message='Successfully created your account. Welcome to lunchbox. :D Please sign in')
    
    return render_template('create_account.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
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
        
        page='meals'
        if user.user_type == 'chef':
            page = 'todays_menu'

        return redirect(url_for('home', page=page))

    return render_template('login.html')


@app.route('/home/<page>', methods=['GET'])
def home(page):
    user = get_user_by_email(session['email'])
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
    if orders != None:
        orders_dicts = {}
        chefs_for_orders = {}
        for order in orders:
            chefs_for_orders[order.id] = get_user_by_id(order.chef_id)

        orders_dicts = orders_to_dicts(orders, chefs_for_orders)

    chefs = get_users_by_ids(meals_dicts.keys())

    return render_template('user_home.html', user_profile=user_profile, meals_dicts=meals_dicts, chefs=chefs, page=page, orders_dicts=orders_dicts)


@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        pic_url = upload_pic(request.files['item_picture'], session['user_id'], request.form['item_name'])
        create_new_item(request.form, session['user_id'], pic_url)
        return redirect(url_for('home', page='items'))


@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
    if request.method == 'POST':
        pic_url = upload_pic(request.files['profile_pic'], session['user_id'], request.form['first_name_in'])
        update_user(request.form, session['user_id'], pic_url)
        return redirect(url_for('home', page='profile', message='Successfully updated profile'))


@app.route('/add_meal', methods=['POST', 'GET'])
def add_meal():
    if request.method == 'POST':
        add_new_meal(request.form, session['user_id'])
        return redirect(url_for('home', page='todays_menu'))


@app.route('/place_order', methods=['POST', 'GET'])
def place_order():
    if request.method == 'POST':
        place_new_order(request.form, session['user_id'])
        return redirect(url_for('home', page='orders'))

if __name__ == '__main__':
    app.run(debug=True)