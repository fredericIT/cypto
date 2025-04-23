from flask import Blueprint, redirect,url_for,render_template, request, session

account_bprt= Blueprint("account",__name__, url_prefix="/account")