from flask import Flask, redirect, url_for,send_from_directory
from db import db
from blueprints.auth import auth_bprt
from blueprints.dashboard import dash_bprt
from blueprints.account import account_bprt
from blueprints.trading import trading_bprt
from blueprints.user import user_bprt
from blueprints.admin import admin_bprt
from db.models import *  
from flask_migrate import Migrate
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login" 
login_manager.login_message = "Login Required to access this resource."
login_manager.login_message_category = "warning"
app.register_blueprint(auth_bprt)
app.register_blueprint(dash_bprt)
app.register_blueprint(account_bprt)
app.register_blueprint(trading_bprt)
app.register_blueprint(user_bprt)
app.register_blueprint(admin_bprt)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.jpg', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   
    app.run(debug=True)
