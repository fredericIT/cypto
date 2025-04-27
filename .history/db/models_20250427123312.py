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

    # Updated relationships
    kyc = db.relationship('KYC', back_populates='user', uselist=False, cascade='all, delete-orphan')
    account = db.relationship('Account', back_populates='user', uselist=False, cascade='all, delete-orphan')
    btc_wallet = db.relationship('BTCWallet', back_populates='user', cascade='all, delete-orphan', uselist=False)
    eth_wallet = db.relationship('ETHWallet', back_populates='user', cascade='all, delete-orphan', uselist=False)
    usdt_wallet = db.relationship('USDTWallet', back_populates='user', cascade='all, delete-orphan', uselist=False)
    bnb_wallet = db.relationship('BNBWallet', back_populates='user', cascade='all, delete-orphan', uselist=False)
    notifications = db.relationship('Notification', back_populates='user', uselist=False, cascade='all, delete-orphan')

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
    __tablename__ = 'kyc_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    document_front_path = db.Column(db.String(255), nullable=False)
    document_back_path = db.Column(db.String(255))
    selfie_with_id_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewer_notes = db.Column(db.Text)
    
    user = db.relationship('User', back_populates='kyc')
    
    def __repr__(self):
        return f'<KYC {self.id} - {self.status}>'


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

 

# models.py
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(20), default='info')  # info, success, warning, danger
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link = db.Column(db.String(255))  # Optional link for action
    
    # Changed backref name to avoid conflict
    user = db.relationship('User', backref=db.backref('user_notifications', lazy=True, order_by='Notification.created_at.desc()'))
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'is_read': self.is_read,
            'date': self.created_at.strftime('%Y-%m-%d'),
            'time': self.created_at.strftime('%H:%M'),
            'link': self.link
        }



class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.OPEN)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    admin_notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('support_tickets', lazy=True))
    replies = db.relationship('TicketReply', backref='ticket', lazy=True, order_by='TicketReply.created_at')
    
    def __repr__(self):
        return f'<SupportTicket {self.id} - {self.subject}>'

class TicketReply(db.Model):
    __tablename__ = 'ticket_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_admin_reply = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<TicketReply {self.id} - {self.message[:50]}>'