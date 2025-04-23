from flask import Blueprint, redirect,url_for,render_template, request, session
from flask_login import current_user
import random

trading_bprt= Blueprint("trading",__name__, url_prefix="/trading")


    

@trading_bprt.route('/trade',methods=["GET", "POST"])
def trade():
    if request.method=="POST":
        traded_amount= request.json.get("amount")
        direction= request.json.get("direction")
        profit= traded_amount * 0.12
    balances= {
                'BTC': current_user.account.BTC,
                'ETH': current_user.account.ETH,
                'USDT':current_user.account.USDT,
                'BNB': current_user.account.BNB
            }
    return render_template('user/trade.html', balances=balances)

