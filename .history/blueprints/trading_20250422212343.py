from flask import Blueprint, redirect,url_for,render_template, request, session,jsonify
from flask_login import current_user
import random
from db.models import User, Transaction
from error_handler.db import handle_sqlalchemy_error 
from app_types import Coins
from decimal import Decimal
from datetime import datetime
from db import db

trading_bprt= Blueprint("trading",__name__, url_prefix="/trading")


    

@trading_bprt.route('/trade',methods=["GET", "POST"])
# @handle_sqlalchemy_error('trading.trade')
def trade():
    if request.method=="POST":
        traded_amount= request.json.get("amount")
        direction= request.json.get("direction")
        traded_coin= request.json.get("coin")
        profit= traded_amount * 0.12
        
        coin= Coins(traded_coin)
        balance = Decimal(str(getattr(current_user.account, traded_coin, 0)))
        
        try:
            setattr(current_user.account, traded_coin, balance +profit)
 

            transaction = Transaction(
                sender_id=current_user.id,
                receiver_id=current_user.id,
                amount=print,
                coin=coin.name,
                status='completed',
                completed_at=datetime.utcnow()
            )
            db.session.add(transaction)
            
            db.session.commit()
            
            return  jsonify({
                "success":True, 
                "message":f"The traded amount is {traded_amount} and profit is {profit} balance is {balance}",
                "profit":profit,
                "total": traded_amount
                },)
            
        except Exception as e:
            db.session.rollback()
            return  jsonify({
                "success":False, 
                "message":f'Transfer failed: {str(e)}',
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

