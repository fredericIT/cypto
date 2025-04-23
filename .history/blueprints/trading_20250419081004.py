from flask import Blueprint, redirect,url_for,render_template, request, session

trading_bprt= Blueprint("trading",__name__, url_prefix="/trading")


@trading_bprt.route('/trade')
def trade():
    return render_template('user/trade.html')