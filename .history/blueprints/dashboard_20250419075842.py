from flask import Blueprint, redirect,url_for,render_template, request, session

dash_bprt= Blueprint("dash",__name__, url_prefix="/dash")