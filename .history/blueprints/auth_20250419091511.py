from flask import Blueprint, redirect,url_for,render_template, request, session,flash
from db.models import User
from db import db

auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")


@auth_bprt.route("/", methods=["GET", "POST"])
def auth():
   return redirect(url_for('auth.login'))

@auth_bprt.route("/register",methods=["GET","POST"])
def register():
    if request.method == 'POST':
        try:
            

            user = User(
                full_name=request.form['full_name'],
                email=request.form["email"],
                password = request.form['password'],
                withdraw_password = request.form['withdraw_password']
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            flash(f'Creation of new user account failed! {str(e)}', 'danger')
            return redirect(url_for("auth.register")),500
         
        flash('Account creation done successfully!', 'success'), 200
        return redirect(url_for("auth.register")), 200
    return render_template('register.html')


@auth_bprt.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user (database logic will be added later)
        print(f"Login attempt: {email}")

        # Simulate login success
        session['user'] = email

        if 'admin' in email.lower():
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dash.dashboard'))
    
    return render_template('login.html')



@auth_bprt.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))