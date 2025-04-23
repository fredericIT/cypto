from flask import Blueprint, redirect
login_bprt= Blueprint("login",__name__, url_prefix="/login")

@login_bprt.route("/")
def login():
    return red