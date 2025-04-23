from dotenv import load_dotenv
load_dotenv()
from flask import Flask, flash, render_template, request, redirect, url_for, session
from alchemy import db
from blueprints.auth  import  auth_bprt
from blueprints.dashboard import dash_bprt
from blueprints.account import account_bprt

app = Flask(__name__)
app.config.from_object("config.Config")
app.register_blueprint(auth_bprt)
app.register_blueprint(dash_bprt)
app.register_blueprint(account_bprt)
db.init_app(app)



# Home redirects to login
@app.route('/')
def home():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
