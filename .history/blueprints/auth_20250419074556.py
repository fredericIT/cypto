from flask import Blueprint, redirect,url_for
auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")

@auth_bprt.route("/login")
def login():
    return redirect(url_for('auth_bprt.register'))

@auth_bprt.route("/register")
def register():
    return redirect(url_for('auth_bprt.login'))