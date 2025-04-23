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


    

@trading_bprt.route('/trade', methods=["GET", "POST"])
def trade():
    if request.method == "POST":
        try:
            traded_amount = Decimal(str(request.json.get("amount")))
            direction = request.json.get("direction")
            traded_coin = request.json.get("coin")
            print("Coin: ", traded_coin)

            profit = traded_amount * Decimal("0.12")

            coin_enum = Coins(traded_coin)  # Ensure Coins is a valid Enum or class
            balance = Decimal(str(getattr(current_user.account, traded_coin, 0)))

            # Update user's balance
            setattr(current_user.account, coin_enum.name, balance + profit)

            # Create transaction record
            transaction = Transaction(
                sender_id=current_user.id,
                receiver_id=current_user.id,
                amount=traded_amount,
                coin=coin_enum.name,
                status='completed',
                completed_at=datetime.utcnow()
            )
            db.session.add(transaction)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": f"The traded amount is {traded_amount} and profit is {profit}, previous balance was {balance}",
                "profit": float(profit),
                "total": float(traded_amount)
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f'Transfer failed: {str(e)}',
                "profit": 0,
                "total": request.json.get("amount")
            })

    balances = {
        'BTC': [current_user.account.BTC, Coins.BTC],
        'ETH': [current_user.account.ETH, Coins.ETH],
        'USDT': [current_user.account.USDT, Coins.USDT],
        'BNB': [current_user.account.BNB, Coins.BNB]
    }
    return render_template('user/trade.html', balances=balances)


