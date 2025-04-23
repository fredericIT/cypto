from flask import Blueprint, redirect,url_for,render_template, request, session, flash

from flask_login import login_required,current_user
from app_types import Coins
from db.models import User,Account,BNBWallet,BTCWallet,USDTWallet, ETHWallet
from db import db
account_bprt= Blueprint("account",__name__, url_prefix="/account")


@account_bprt.route('/deposit')
@login_required
def deposit():
    return render_template('user/deposit.html')

@account_bprt.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
       
        withdraw_address = request.form['withdraw_address']
        coin = request.form['coin']
        amount = float(request.form['amount'])
        withdraw_password = request.form['withdraw_password']
        
        flash('✅ Withdrawal request submitted successfully!', 'success')
        return redirect(url_for('account.withdraw'))

    return render_template('user/withdraw.html', coins= Coins)


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