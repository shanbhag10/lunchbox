from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
Session(app)

from db.user import *
from db.item import *
from controller.user import *
from controller.item import *
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
        
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/home', methods=['GET'])
def home():
    user = get_user_by_email(session['email'])
    user_profile = user_to_dict(user)

    items = get_items_for_chef(session['user_id'])
    items_dicts = items_to_dict(items)

    return render_template('chef_home.html', user_profile=user_profile, items_dicts=items_dicts)

@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        pic_url = upload_pic(request.files)
        create_new_item(request.form, session['user_id'], pic_url)
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)