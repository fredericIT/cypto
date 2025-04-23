from db import db   
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    withdraw_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    kyc = db.relationship('KYC', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.email} | Role: {self.role}>"
    
class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    account_status = db.Column(db.String(50), nullable=False)   
    
    BTC = db.Column(db.Numeric(precision=18, scale=8), nullable=True, default=0)   
    ETH = db.Column(db.Numeric(precision=18, scale=8), nullable=False,default=0)
    USDT = db.Column(db.Numeric(precision=18, scale=2), nullable=True,default=0)   
    BNB = db.Column(db.Numeric(precision=18, scale=8), nullable=True,default=0)

    user = db.relationship('User', back_populates='account')


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
