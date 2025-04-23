from flask import Blueprint, redirect,url_for,render_template, request, session

from flask_login import login_required,current_user

dash_bprt= Blueprint("dash",__name__, url_prefix="/dash")

@dash_bprt.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    user_info = {
            'full_name': current_user.email,
            'email': current_user.email,
            'balances': {
                'BTC': 0.0,
                'ETH': 0.0,
                'USDT': 0.0,
                'BNB': 0.0
            },
            'deposit_addresses': {
                'BTC': 'bc1qrynf3yt0w524mtca7q0t8hs4ufpd8fj5dg2855',
                'ETH': '0xe184F8F7112bF1471b9c4452Efb7Bf9E5ddb7df1',
                'USDT': '0xe184F8F7112bF1471b9c4452Efb7Bf9E5ddb7df1',
                'BNB': '0xe184F8F7112bF1471b9c4452Efb7Bf9E5ddb7df1'
            }
        }
    return render_template('user/dashboard.html', user=user_info)