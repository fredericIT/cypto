from flask import Blueprint, redirect,url_for,render_template, request, session, flash

from flask_login import login_required,current_user
from app_types import Coins
from db.models import User,Account,BNBWallet,BTCWallet,USDTWallet, ETHWallet
from db import db
from flask_login import current_user
from error_handler.db import handle_sqlalchemy_error
account_bprt= Blueprint("account",__name__, url_prefix="/account")


@account_bprt.route('/deposit')
@login_required
def deposit():
    return render_template('user/deposit.html')

@account_bprt.route('/withdraw', methods=['GET', 'POST'])
@login_required
@handle_sqlalchemy_error('account.withdraw')
def withdraw():
    if request.method == 'POST':
       
        withdraw_address = request.form['withdraw_address']
        coin = request.form['coin']
        amount = float(request.form['amount'])
        withdraw_password = request.form['withdraw_password']

        coin_enum = Coins(coin)

        
        wallet_models = {
            Coins.BTC: BTCWallet,
            Coins.ETH: ETHWallet,
            Coins.BNB: BNBWallet,
            Coins.USDT: USDTWallet
        }

       
        receiver = wallet_models[coin_enum].query.filter_by(deposit=withdraw_address).first()
        
        if not receiver:
            flash('Receiver address not found!', 'danger')
            return redirect(url_for('account.withdraw'))
 
        user_balance = getattr(current_user.account, coin_enum.name, 0)
        if user_balance < amount:
            flash(f'Insufficient funds of {coin_enum.value}. Please recharge your account and try again!', 'danger')
            return redirect(url_for('account.withdraw'))

        if not withdraw_password == current_user.withdraw_password:
            flash('Withdraw password is incorrect!', 'danger')
            return redirect(url_for('account.withdraw'))
 
        try:
            
            setattr(current_user.account, coin_enum.name, user_balance - amount)
            db.session.commit()
            
            flash(f'Successfully withdrew {amount} {coin_enum.value}!', 'success')
            return redirect(url_for('account.withdraw'))
        except Exception as e:
            db.session.rollback()
            flash(f'Withdrawal failed: {str(e)}', 'danger')
            return redirect(url_for('account.withdraw'))

    return render_template('user/withdraw.html', coins=Coins)


@account_bprt.route('/transactions')
@login_required
def transactions():
    # Example transactions (later you will load from database)
    transactions = [
        {"type": "Deposit", "coin": "BTC", "amount": "0.005", "status": "Completed", "date": "2025-04-17"},
        {"type": "Withdraw", "coin": "ETH", "amount": "0.2", "status": "Pending", "date": "2025-04-16"},
        {"type": "Trade Profit", "coin": "USDT", "amount": "12", "status": "Completed", "date": "2025-04-15"},
    ]
    return render_template('user/transaction_history.html', transactions=transactions)