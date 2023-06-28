from flask_wtf import FlaskForm
from wtforms import Form, TextAreaField, validators, StringField, SubmitField, IntegerField, DateField, RadioField, \
    DecimalField, BooleanField, EmailField, PasswordField
from wtforms.validators import InputRequired
from sqlalchemy import desc, asc


class RegForm(FlaskForm):
    name_form = StringField('Имя', validators=[validators.DataRequired()])
    last_name_form = StringField('Фамилия', validators=[validators.DataRequired()])
    email_form = EmailField('Логин (email)', [validators.DataRequired(), validators.Email()])
    password_form = PasswordField('Пароль',id='pswd', validators=[validators.DataRequired()])
    show_password = BooleanField('Показать пароль', id='check')
    # submit = SubmitField('Сохранить')

class LoginForm(FlaskForm):
    email_form = EmailField('Логин (email)', [validators.DataRequired(), validators.Email()])
    password_form = PasswordField('Пароль', validators=[validators.DataRequired()])
    remember = BooleanField('Запомнить')