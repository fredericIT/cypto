from flask import Blueprint, redirect,url_for,render_template
auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")


@auth_bprt.route("/", methods=["GET", "POST"])
def auth():
   return redirect(url_for('auth.login'))

@auth_bprt.route("/login", methods=["GET","POST"])
def login():
    return  render_template('login.html')

@auth_bprt.route("/register",methods=["GET","POST"])
def register():
    return  render_template('register.html')