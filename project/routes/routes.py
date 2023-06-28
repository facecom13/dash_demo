from flask import Blueprint, session, render_template, redirect, url_for, abort, request, jsonify, flash
from models.models import users
import forms.forms as forms_1
import os
import sqlalchemy
from sqlalchemy import desc, asc
import pandas as pd
from datetime import datetime
import requests
import json
from flask_login import login_user, login_required, current_user, logout_user

from extensions import extensions

# from sqlalchemy import desc, asc, func
# from sqlalchemy import and_, or_
# from flask_socketio import SocketIO, emit
# from datetime import datetime

db = extensions.db
# db.create_all()
# db.session.commit()
home = Blueprint('home', __name__, template_folder='templates')

socketio = extensions.socketio


@home.route('/index')
def index():
    return render_template('index.html')

@home.route('/')
def main():
    return redirect(url_for('/dash/'))

@home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))



@home.route('/profile')
@login_required
def profile():

    return render_template('profile.html', name=current_user.user_name)

@home.route('/login')
def login():
    form = forms_1.LoginForm()
    return render_template('login.html', form=form)

@home.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    form = forms_1.LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email_form')
        password = request.form.get('password_form')
        remember = True if request.form.get('remember') else False

        user_data = users.query.filter_by(login=email).first()

        if not user_data or password != user_data.user_password:
            flash('Please check your login details and try again.')
            return redirect(url_for('home.login'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user_data, remember=remember)
        # return redirect(url_for('home.profile'))
        return redirect(url_for('/dash/'))
    return redirect(url_for('home.login'))



############ список юзеров ##################
@home.route('/users')
def users_view():
    # user = userdb.query.filter_by(email=email).first()

    users_data = users.query.all()
    return render_template('users.html', users=users_data)


#######  /sighnup страница регистрации ############
@home.route('/sighnup')
def sighnup_view():

    form = forms_1.RegForm()


    # try:
    data_ = session.get('data_')
    if data_:
        data_['type'] = str(type(data_))
    # if 'dict' in str(type(data_)):
    data = json.dumps(data_)
    # except:
    #     pass
    # session.clear()
    session['data_'] = {
        'user_name': '',
        'user_last_name': '',
        'user_login': '',
        'user_password': '',
        'login_message':''
    }

    return render_template('sighnup.html', form = form, data=data)

# if request.method == 'POST':

@home.route('/registration', methods=["POST", "GET"])
def registration_view():
    form = forms_1.RegForm()

    if form.validate_on_submit():
        user_name = form.name_form.data,
        user_last_name = form.last_name_form.data
        user_login = form.email_form.data
        user_password = form.password_form.data

        # Получаем данные из таблицы users
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = sqlalchemy.create_engine(url_db)
        login_list = []
        df_users = pd.DataFrame()
        last_user_id = 0
        try:
            with engine.connect() as con:
                query = 'SELECT *  FROM "users";'
                df_users = pd.read_sql(query, con)
            last_user_id = df_users['id'].max()

            login_list = df_users['login'].unique()
        except:
            pass
        new_user_id = last_user_id + 1
        # session.clear()
        if user_login in login_list:
            session['data_'] = {
                'user_name': user_name,
                'user_last_name': user_last_name,
                'user_login': user_login,
                'user_password': user_password,
                'login_message': f'{user_login} уже используется'
            }
        else:
            new_user_data = [
                {
                    'id': new_user_id,
                    'user_name': user_name,
                    'user_last_name': user_last_name,
                    'login': user_login,
                    'user_password': user_password
                }
            ]
            new_user_df = pd.DataFrame(new_user_data)
            df_users = pd.concat([df_users, new_user_df])
            with engine.connect() as con:
                df_users.to_sql(
                    name="users",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists='replace'
                )



        return redirect(url_for('home.sighnup_view'))
        # return render_template('sighnup.html', form=form, data =data)

    else:
        print("форма не валидировалась")
        return redirect(url_for('home.sighnup_view'))
