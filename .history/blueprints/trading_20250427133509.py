from flask import Blueprint, redirect,url_for,render_template, request, session,jsonify
from flask_login import current_user
import random
from db.models import User, Transaction
from error_handler.db import handle_sqlalchemy_error 
from app_types import Coins
from decimal import Decimal
from datetime import datetime
from db import db
from db.models import Account
from flask_login import login_required

trading_bprt= Blueprint("trading",__name__, url_prefix="/trading")


    
@trading_bprt.route('/trade', methods=["GET", "POST"])
@login_required
def trade():
    session.pop('_flashes', None)
    if request.method == "POST":
        try:
            traded_amount = Decimal(str(request.json.get("amount")))
            traded_coin = request.json.get("coin")
            print("Coin: ", traded_coin)

            profit = traded_amount * Decimal("0.12")
            print(f"Calculated profit: {profit}")

            coin_enum = Coins(traded_coin)
            
            # Explicitly fetch current user's account from the database
            user_account = Account.query.filter_by(user_id=current_user.id).first()
            if user_account is None:
                raise ValueError("User account not found.")

            # Fetch the balance from the account
            balance = Decimal(str(getattr(user_account, traded_coin, 0)))
            print(f"Current balance for {traded_coin}: {balance}")

            # Add profit to the existing balance
            new_balance = balance + profit
            print(f"New balance after adding profit: {new_balance}")

            # Update the balance in the user's account
            setattr(user_account, coin_enum.name, new_balance)

            # Commit the updated balance to the database
            db.session.add(user_account)
            db.session.commit()

            # Ensure the balance was updated correctly
            updated_balance = getattr(user_account, coin_enum.name)
            print(f"Updated balance for {traded_coin}: {updated_balance}")

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

            # Commit the transaction
            db.session.commit()

            # Log the final state after commit
            print(f"Transaction committed. Final balance for {traded_coin}: {updated_balance}")

            return jsonify({
                "success": True,
                "message": f"Profit of {profit} added successfully. Previous balance was {balance}, new balance is {new_balance}",
                "profit": float(profit),
                "new_balance": float(new_balance)
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")
            return jsonify({
                "success": False,
                "message": f'Transaction failed: {str(e)}',
                "profit": 0,
                "new_balance": float(getattr(user_account, traded_coin, 0)) if 'traded_coin' in locals() else 0
            })

    # GET request handling remains the same
    balances = {
        'BTC': [current_user.account.BTC, Coins.BTC],
        'ETH': [current_user.account.ETH, Coins.ETH],
        'USDT': [current_user.account.USDT, Coins.USDT],
        'BNB': [current_user.account.BNB, Coins.BNB]
    }
    return render_template('user/trade.html', balances=balances)



