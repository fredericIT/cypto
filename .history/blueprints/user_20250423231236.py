from flask import Blueprint, redirect,url_for,render_template, request, session, flash
from flask_login import login_required, current_user
from db import db
import  bcrypt

user_bprt= Blueprint("user",__name__, url_prefix="/user")
@user_bprt.route('/')
@user_bprt.route('/profile')
def profile():
    return render_template('user/profile.html', user=current_user)

@user_bprt.route('/kyc', methods=['GET', 'POST'])
def kyc():
    session.pop('_flashes', None)
    if request.method == 'POST':
        full_name = request.form['full_name']
        document_type = request.form['document_type']
        document_front = request.files['document_front']
        document_back = request.files.get('document_back')  # Optional
        selfie_with_id = request.files['selfie_with_id']

        # Here you would save these files
        # Example (you can customize):
        # document_front.save(f'static/uploads/kyc/{full_name}_front.jpg')
        # selfie_with_id.save(f'static/uploads/kyc/{full_name}_selfie.jpg')

        flash('✅ KYC documents submitted successfully!', 'success')
        return redirect(url_for('kyc'))

    return render_template('user/kyc.html')

@user_bprt.route('/notifications')
def notifications():
    session.pop('_flashes', None)
    # Example notification data
    notifications = [
        {"title": "KYC Approved ✅", "message": "Your identity verification has been approved.", "date": "2025-04-17", "type": "success"},
        {"title": "Withdrawal Request Sent 💸", "message": "We received your withdrawal request.", "date": "2025-04-16", "type": "info"},
    ]
    return render_template('user/notifications.html', notifications=notifications)
@user_bprt.route('/support', methods=['GET', 'POST'])
def support():
    session.pop('_flashes', None)
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']

        # You can save the ticket to database or email it to admin

        flash('✅ Your support request has been submitted!', 'success')
        return redirect(url_for('support'))

    return render_template('user/support.html')

@user_bprt.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    full_name = request.form.get('full_name')
    password = request.form.get('password')
    withdraw_password = request.form.get('withdraw_password')

 
    current_user.full_name = full_name

 
    if password:
        current_user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

 
    if withdraw_password:
        current_user.withdraw_password =  withdraw_password

    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating your profile.', 'danger')

    return redirect(url_for('user.profile'))   
