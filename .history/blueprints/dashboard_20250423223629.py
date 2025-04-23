from flask import Blueprint, redirect,url_for,render_template, request, session

from flask_login import login_required,current_user
from  db.models import Account

dash_bprt= Blueprint("dash",__name__, url_prefix="/dash")

@dash_bprt.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
   session.pop('_flashes', None)
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
                'BTC': current_user.btc_wallet.deposit,
                'ETH': current_user.eth_wallet.deposit,
                'USDT': current_user.usdt_wallet.deposit,
                'BNB': current_user.bnb_wallet.deposit
            }
        }
    return render_template('user/dashboard.html', user=user_info)