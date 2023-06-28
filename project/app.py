from flask import Flask, render_template, request, flash
from extensions import extensions
from routes.routes import home
import os
from dash_application import create_dash_application
from dash_application_retail import create_dash_application_retail
from flask_login import LoginManager
from models.models import users
import os
import sqlalchemy
import pandas as pd
db_dir = os.path.abspath(os.path.dirname(__file__)) + "/database"
from flask_login import login_user, login_required

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/fms_v3_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@db:5432/postgres'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_dir, 'datab.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:zh2311@db:5432/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'




# os.environ["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(db_dir, 'datab.db')
os.environ["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:zh2311@db:5432/postgres'
os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"] = 'postgresql+psycopg2://postgres:zh2311@db:5432/postgres'
os.environ["SQLITE_URL"] = '//' + os.path.join(db_dir, 'datab.db')
os.environ["leasing_source_table"] = 'leasing_temp_db'


db = extensions.db

migrate = extensions.migrate
socketio = extensions.socketio

create_dash_application(app)
app_dash = create_dash_application_retail(app)

socketio.init_app(app)

db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)

app.register_blueprint(home)

login_manager = LoginManager()
login_manager.login_view = 'home.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return users.query.get(int(user_id))

df = pd.DataFrame()
for view_func in app.view_functions:
    list_data = [
        {
            'view_func': str(view_func),
            'app_dash.url_base_pathname': str(app_dash.config['url_base_pathname'])
        }
    ]
    temp_df = pd.DataFrame(list_data)
    df = pd.concat([df, temp_df])
    for view_func in app.view_functions:
        # if view_func.startswith(app_dash.config['url_base_pathname']):
        if view_func.startswith('dash'):
            app.view_functions[view_func] = login_required(app.view_functions[view_func])


url_db = 'postgresql+psycopg2://postgres:zh2311@db:5432/postgres'
engine = sqlalchemy.create_engine(url_db)
with engine.connect() as con:
    df.to_sql(
        name="view_func",
        con=con,
        # chunksize=1000,
        # method='multi',
        index=False,
        if_exists='replace'
    )

app._favicon = "favicon.ico"

if __name__ == '__main__':
    app.run(debug=True)