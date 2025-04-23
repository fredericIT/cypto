from flask import Blueprint, redirect,url_for,render_template, request, session, flash
from flask_login import login_required, current_user
from db import db
import  bcrypt
from flask import render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from db.models import db, KYC
 

user_bprt= Blueprint("user",__name__, url_prefix="/user")
@user_bprt.route('/')
@user_bprt.route('/profile')
def profile():
    return render_template('user/profile.html', user=current_user)

@user_bprt.route('/kyc', methods=['GET', 'POST'])
@login_required
def kyc():
    session.pop('_flashes', None)
    
    # Check if user already has a KYC submission
    existing_kyc = KYC.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        if existing_kyc and existing_kyc.status == 'approved':
            flash('You already have an approved KYC submission.', 'warning')
            return redirect(url_for('user_bprt.kyc'))
            
        full_name = request.form['full_name']
        document_type = request.form['document_type']
        document_front = request.files['document_front']
        document_back = request.files.get('document_back')  # Optional
        selfie_with_id = request.files['selfie_with_id']
        
        # Validate file extensions
        allowed_extensions = {'jpg', 'jpeg', 'png', 'pdf'}
        
        def allowed_file(filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in allowed_extensions
        
        if not (allowed_file(document_front.filename) and allowed_file(selfie_with_id.filename)):
            flash('Invalid file type. Only JPG, PNG, or PDF allowed.', 'danger')
            return redirect(url_for('user_bprt.kyc'))
            
        if document_back and not allowed_file(document_back.filename):
            flash('Invalid file type for back document. Only JPG, PNG, or PDF allowed.', 'danger')
            return redirect(url_for('user_bprt.kyc'))
        
        # Create upload directory if it doesn't exist
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/kyc')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_id_str = str(current_user.id)
        
        front_filename = f"doc_front_{user_id_str}_{timestamp}.{document_front.filename.rsplit('.', 1)[1].lower()}"
        front_path = os.path.join(upload_folder, secure_filename(front_filename))
        
        selfie_filename = f"selfie_{user_id_str}_{timestamp}.{selfie_with_id.filename.rsplit('.', 1)[1].lower()}"
        selfie_path = os.path.join(upload_folder, secure_filename(selfie_filename))
        
        # Save files
        document_front.save(front_path)
        selfie_with_id.save(selfie_path)
        
        # Handle back document if provided
        back_path = None
        if document_back:
            back_filename = f"doc_back_{user_id_str}_{timestamp}.{document_back.filename.rsplit('.', 1)[1].lower()}"
            back_path = os.path.join(upload_folder, secure_filename(back_filename))
            document_back.save(back_path)
        
        # Create or update KYC record
        if existing_kyc:
            # Update existing record
            existing_kyc.full_name = full_name
            existing_kyc.document_type = document_type
            existing_kyc.document_front_path = front_path
            existing_kyc.document_back_path = back_path
            existing_kyc.selfie_with_id_path = selfie_path
            existing_kyc.status = 'pending'
            existing_kyc.submitted_at = datetime.utcnow()
            existing_kyc.reviewed_at = None
            existing_kyc.reviewer_notes = None
        else:
            # Create new record
            new_kyc = KYC(
                user_id=current_user.id,
                full_name=full_name,
                document_type=document_type,
                document_front_path=front_path,
                document_back_path=back_path,
                selfie_with_id_path=selfie_path,
                status='pending'
            )
            db.session.add(new_kyc)
        
        db.session.commit()
        
        flash('✅ KYC documents submitted successfully! Our team will review them shortly.', 'success')
        return redirect(url_for('user_bprt.kyc'))
    
    return render_template('user/kyc.html', kyc=existing_kyc)

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
