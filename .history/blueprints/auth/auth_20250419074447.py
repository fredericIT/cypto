from flask import Blueprint, redirect
auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")

@auth_bprt.route("/login")
def login():
    return redirect()

@auth_bprt.route("/register")
def login():
    return redirect()