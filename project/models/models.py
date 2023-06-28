from extensions import extensions
from datetime import datetime, date
from flask_login import UserMixin

db = extensions.db

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    user_name = db.Column(db.String)
    user_last_name = db.Column(db.String)
    user_password = db.Column(db.String)

# class leasingdataDB(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     current_agreement_status = db.Column(db.String)
#
#
# class leasingdatademoDB(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


