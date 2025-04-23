from flask import Blueprint, redirect,url_for,render_template, request, session

dash_bprt= Blueprint("trading",__name__, url_prefix="/trading")