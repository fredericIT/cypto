from flask import Blueprint, redirect,url_for,render_template, request, session, flash

from flask_login import login_required,current_user
from app_types import Coins
from db.models import User,Account,BNBWallet,BTCWallet,USDTWallet, ETHWallet,Transaction
from datetime import  datetime
from db import db
from flask_login import current_user
from error_handler.db import handle_sqlalchemy_error
from decimal import Decimal
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
        try:
       
            withdraw_address = request.form['withdraw_address'].strip()
            coin = request.form['coin']
            amount = Decimal(request.form['amount'])
            withdraw_password = request.form['withdraw_password'].strip()
 
            coin_enum = Coins(coin)
            
 
            wallet_models = {
                Coins.BTC: (BTCWallet, 'BTC'),
                Coins.ETH: (ETHWallet, 'ETH'),
                Coins.BNB: (BNBWallet, 'BNB'),
                Coins.USDT: (USDTWallet, 'USDT')
            }
            WalletModel, coin_attr = wallet_models[coin_enum]

    
            sender_balance = Decimal(str(getattr(current_user.account, coin_attr, 0)))
            if sender_balance < amount:
                flash(f'Insufficient {coin_enum.value} balance', 'danger')
                return redirect(url_for('account.withdraw'))

            if withdraw_password != current_user.withdraw_password:
                flash('Invalid withdrawal password', 'danger')
                return redirect(url_for('account.withdraw'))
 
            receiver_wallet = WalletModel.query.filter_by(deposit=withdraw_address).first()
            if receiver_wallet.user.id==current_user.id:
                flash('You can\'t send  crypto to your self', 'danger')
                return redirect(url_for('account.withdraw'))

            if not receiver_wallet:
                flash('Receiver wallet not found', 'danger')
                return redirect(url_for('account.withdraw'))

            receiver_user = receiver_wallet.user

            try:
                setattr(current_user.account, coin_attr, sender_balance - amount)
    
                receiver_account = receiver_user.account
                receiver_balance = Decimal(str(getattr(receiver_account, coin_attr, 0)))
                setattr(receiver_account, coin_attr, receiver_balance + amount)
 
                transaction = Transaction(
                    sender_id=current_user.id,
                    receiver_id=receiver_user.id,
                    amount=amount,
                    coin=coin_enum,
                    status='completed',
                    completed_at=datetime.utcnow()
                )
                db.session.add(transaction)
                
                db.session.commit()
                
                flash(f'Successfully sent {amount} {coin_enum.value}! Transaction ID: {transaction.id}', 'success')
                return redirect(url_for('account.withdraw'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Transfer failed: {str(e)}', 'danger')
                return redirect(url_for('account.withdraw'))

        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
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