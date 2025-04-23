from flask import Blueprint, redirect,url_for,render_template, request, session,jsonify
from flask_login import current_user
import random
from db.models import User
from error_handler.db import handle_sqlalchemy_error 
from app_types import Coins
from decimal import Decimal

trading_bprt= Blueprint("trading",__name__, url_prefix="/trading")


    

@trading_bprt.route('/trade',methods=["GET", "POST"])
# @handle_sqlalchemy_error('trading.trade')
def trade():
    if request.method=="POST":
        traded_amount= request.json.get("amount")
        direction= request.json.get("direction")
        traded_coin= request.json.get("coin")
        profit= traded_amount * 0.12
        
        # coin= Coins(traded_coin)
        balance = Decimal(str(getattr(current_user.account, traded_coin, 0)))
        print("Coinnnnnnnnnnn", balance)
        return  jsonify({
            "success":True, 
            "message":f"The traded amount is {traded_amount} and profit is {profit} balance is {balance}",
             "profit":profit,
             "total": traded_amount
            },)
    balances= {
                'BTC': current_user.account.BTC,
                'ETH': current_user.account.ETH,
                'USDT':current_user.account.USDT,
                'BNB': current_user.account.BNB
            }
    return render_template('user/trade.html', balances=balances)

