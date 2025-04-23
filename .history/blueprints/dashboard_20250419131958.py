from flask import Blueprint, redirect,url_for,render_template, request, session

from flask_login import login_required,current_user
from  db.models import Account

dash_bprt= Blueprint("dash",__name__, url_prefix="/dash")

@dash_bprt.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
   
    user_info = {
            'full_name': current_user.full_name,
            'email': current_user.email,
            'balances': {
                'BTC': current_user.account.BTC,
                'ETH': current_user.account.ETH,
                'USDT':current_user.account.USDT,
                'BNB': current_user.account.BNB
            },
            'deposit_addresses': {
                'BTC': current_user.btc_wallett.deposit,
                'ETH': '0xe184F8F7112bF1471b9c4452Efb7Bf9E5ddb7df1',
                'USDT': '0xe184F8F7112bF1471b9c4452Efb7Bf9E5ddb7df1',
                'BNB': '0xe184F8F7112bF1471b9c4452Efb7Bf9E5ddb7df1'
            }
        }
    return render_template('user/dashboard.html', user=user_info)