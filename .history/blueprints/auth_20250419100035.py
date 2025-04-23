from flask import Blueprint, redirect,url_for,render_template, request, session,flash
from db.models import User
from db import db
from  error_handler.db import handle_sqlalchemy_error
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")


@auth_bprt.route("/", methods=["GET", "POST"])
def auth():
   return redirect(url_for('auth.login'))

@auth_bprt.route("/register",methods=["GET","POST"])
@handle_sqlalchemy_error(redirect_url="auth.register") 
def register():
    if request.method == 'POST': 
        hashed_pwd=bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt()).decode()
        user = User(
            full_name=request.form['full_name'],
            email=request.form["email"],
            password = hashed_pwd,
            withdraw_password = request.form['withdraw_password']
        )
        db.session.add(user)
        db.session.commit()
        
         
        flash('Account creation done successfully!', 'success')
        return redirect(url_for("auth.login"))
    return render_template('register.html')


@auth_bprt.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(user.password)
        if user and bcrypt.checkpw(password.encode(),  user.password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dash.dashboard')) 
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')



@auth_bprt.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))