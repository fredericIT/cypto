from db import db   

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=False)
    withdraw_password = db.Column(db.String(255), nullable=False, unique=False)

    kyc = db.relationship('KYC', back_populates='user', uselist=False, cascade='all, delete-orphan')

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
