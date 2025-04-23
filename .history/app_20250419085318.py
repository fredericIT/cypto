 
from flask import Flask , redirect, url_for
from db import db
from blueprints.auth  import  auth_bprt
from blueprints.dashboard import dash_bprt
from blueprints.account import account_bprt
from blueprints.trading import trading_bprt
from blueprints.user import user_bprt
from blueprints.admin import admin_bprt
from db.models import *



def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
  
    db.init_app(app)

    app.register_blueprint(auth_bprt)
    app.register_blueprint(dash_bprt)
    app.register_blueprint(account_bprt)
    app.register_blueprint(trading_bprt)
    app.register_blueprint(user_bprt)
    app.register_blueprint(admin_bprt)

    with app.app_context():
        print(db.engine.table_names())
        db.create_all()  

    return app
app= create_app()

# Home redirects to login
@app.route('/')
def home():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
