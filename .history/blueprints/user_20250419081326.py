from flask import Blueprint, redirect,url_for,render_template, request, session

user_bprt= Blueprint("user",__name__, url_prefix="/user")