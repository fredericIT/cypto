from flask import Blueprint, redirect,url_for,render_template, request, session

dash_bprt= Blueprint("dash",__name__, url_prefix="/dash")

# Dashboard page (after login)
@dash_bprt.route('/dashboard')
def dashboard():
    if 'user' in session:
        user_info = {
            'full_name': 'John Doe',
            'email': session['user'],
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
    else:
        return redirect(url_for('auth.login'))