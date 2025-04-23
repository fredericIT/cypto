from flask import Blueprint, redirect,url_for,render_template, request, session,flash
from db.models import User,Account,BNBWallet,BTCWallet,USDTWallet, ETHWallet

from db import db
from  error_handler.db import handle_sqlalchemy_error
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt
from generators.wallet_address import *
from app_types import *

auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")


@auth_bprt.route("/", methods=["GET", "POST"])
def auth():
   return redirect(url_for('auth.login'))

@auth_bprt.route("/register",methods=["GET","POST"])
@handle_sqlalchemy_error(redirect_url="auth.register") 
def register():
    if request.method == 'POST': 
        hashed_pwd=bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt()).decode()
        user = User(
            full_name=request.form['full_name'],
            email=request.form["email"],
            password = hashed_pwd,
            withdraw_password = request.form['withdraw_password']
        )
        db.session.add(user)
        db.session.flush()
        
        account = Account(user_id=user.id, account_status='active', ETH=0.25)
        btc_d_address, btc_d_private_key = generate_btc_address()
        btc_w_address, btc_w_private_key = generate_btc_address()
        eth_d_address, eth_d_private_key = generate_eth_address()
        eth_w_address, eth_w_private_key = generate_eth_address()
        bnb_d_address, bnb_d_private_key = generate_bnb_address()
        bnb_w_address, bnb_w_private_key = generate_bnb_address()
        tron_d_usdt_address, tron_d_private_key = generate_tron_address()
        tron_w_usdt_address, tron_w_private_key = generate_tron_address()
 
        BTC_address = BTCWallet(
            user_id=user.id,
            coin=Coins.BTC,
            deposit=btc_d_address,
            withdraw=btc_w_address,
            deposit_key=btc_d_private_key,
            withdraw_key=btc_w_private_key
        )

        BNB_address = BNBWallet(
            user_id=user.id,
            deposit=bnb_d_address,
            withdraw=bnb_w_address,
            deposit_key=bnb_d_private_key,
            withdraw_key=bnb_w_private_key
        )

        USDT_address = USDTWallet(
            user_id=user.id,
            deposit=tron_d_usdt_address,
            withdraw=tron_w_usdt_address,
            deposit_key=tron_d_private_key,
            withdraw_key=tron_w_private_key
        )

        ETH_address = ETHWallet(
            user_id=user.id,
            deposit=eth_d_address,
            withdraw=eth_w_address,
            deposit_key=eth_d_private_key,
            withdraw_key=eth_w_private_key
        )
       
        db.session.add_all([account,BTC_address, BNB_address, USDT_address, ETH_address])
        db.session.commit()
        
         
        flash('Account creation done successfully!', 'success')
        return redirect(url_for("auth.login"))
    return render_template('register.html')


 
@auth_bprt.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dash.dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')




@auth_bprt.route('/logout')
def logout():
    logout_user()  
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))