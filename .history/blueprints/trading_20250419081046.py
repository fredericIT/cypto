from flask import Blueprint, redirect,url_for,render_template, request, session

trading_bprt= Blueprint("trading",__name__, url_prefix="/trading")


@trading_bprt.route('/trade')
def trade():
    return render_template('user/trade.html')


@trading_bprt.route('/transaction_history')
def transactions():
    # Example transactions (later you will load from database)
    transactions = [
        {"type": "Deposit", "coin": "BTC", "amount": "0.005", "status": "Completed", "date": "2025-04-17"},
        {"type": "Withdraw", "coin": "ETH", "amount": "0.2", "status": "Pending", "date": "2025-04-16"},
        {"type": "Trade Profit", "coin": "USDT", "amount": "12", "status": "Completed", "date": "2025-04-15"},
    ]
    return render_template('user/transaction_history.html', transactions=transactions)