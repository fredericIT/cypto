from db import db   
from flask_login import UserMixin
from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAlchemyEnum
from app_types import *

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    withdraw_password = db.Column(db.String(255), nullable=False)
    role = db.Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.USER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    kyc = db.relationship('KYC', back_populates='user', uselist=False, cascade='all, delete-orphan')
    account = db.relationship('Account', back_populates='user', uselist=False)
    btc_wallet = db.relationship('BTCWallet', back_populates='user', cascade='all, delete-orphan', uselist=False)
    eth_wallet = db.relationship('ETHWallet', back_populates='user', cascade='all, delete-orphan',uselist=False)
    usdt_wallet = db.relationship('USDTWallet', back_populates='user', cascade='all, delete-orphan',uselist=False)
    bnb_wallet= db.relationship('BNBWallet', back_populates='user', cascade='all, delete-orphan',uselist=False)

    def __repr__(self):
        return f"<User {self.email} | Role: {self.role}>"

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    account_status = db.Column(db.String(50), nullable=False)   
    
    BTC = db.Column(db.Numeric(precision=18, scale=8), nullable=True, default=0)   
    ETH = db.Column(db.Numeric(precision=18, scale=8), nullable=False, default=0)
    USDT = db.Column(db.Numeric(precision=18, scale=2), nullable=True, default=0)   
    BNB = db.Column(db.Numeric(precision=18, scale=8), nullable=True, default=0)

    user = db.relationship('User', back_populates='account')

# Crypto Wallet Models
class BTCWallet(db.Model):
    __tablename__ = 'btc_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,  unique=True)
    deposit = db.Column(db.String(255), nullable=False)
    withdraw= db.Column(db.String(255), nullable=False)
    deposit_key = db.Column(db.String(255), nullable=False)
    withdraw_key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='btc_wallet')

class ETHWallet(db.Model):
    __tablename__ = 'eth_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    deposit = db.Column(db.String(255), nullable=False)
    withdraw = db.Column(db.String(255), nullable=False)
    deposit_key = db.Column(db.String(255), nullable=False)
    withdraw_key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='eth_wallet')

class USDTWallet(db.Model):
    __tablename__ = 'usdt_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,unique=True)
    deposit = db.Column(db.String(255), nullable=False)
    withdraw = db.Column(db.String(255), nullable=False)
    deposit_key = db.Column(db.String(255), nullable=False)
    withdraw_key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    network = db.Column(db.String(50), nullable=False, default='TRC20')  # Could be ERC20 or TRC20
    
    user = db.relationship('User', back_populates='usdt_wallet')

class BNBWallet(db.Model):
    __tablename__ = 'bnb_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    deposit = db.Column(db.String(255), nullable=False)
    withdraw = db.Column(db.String(255), nullable=False)
    deposit_key = db.Column(db.String(255), nullable=False)
    withdraw_key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='bnb_wallet')

class KYC(db.Model):
    __tablename__ = 'kyc'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    kyc_status = db.Column(db.String(50), nullable=False)
    kyc_document = db.Column(db.String(255), nullable=True)
    document_type = db.Column(db.String(100), nullable=False)
    front_image = db.Column(db.String(255), nullable=True)
    back_image = db.Column(db.String(255), nullable=True)
    user_with_document_image = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', back_populates='kyc')


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=18, scale=8), nullable=False)
    coin = db.Column(SQLAlchemyEnum(Coins), nullable=False)   
    status = db.Column(db.String(20), nullable=False, default='pending')   
    tx_hash = db.Column(db.String(255), nullable=True)  
    network_fee = db.Column(db.Numeric(precision=18, scale=8), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
   
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_transactions')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_transactions')