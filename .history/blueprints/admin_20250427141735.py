from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from flask_login import login_required, current_user
from datetime import datetime
from db.models import db, User, Account, KYC, SupportTicket, TicketReply, Transaction, Notification, BNBWallet,BTCWallet,USDTWallet, ETHWallet
from db.models import TicketStatus, UserRole
from sqlalchemy import or_

admin_bprt = Blueprint("admin", __name__, url_prefix="/admin")

# Admin Dashboard
@admin_bprt.route('/')
@admin_bprt.route('/dashboard')
@login_required
def admin_dashboard():
    session.pop('_flashes', None)
    
    # Get counts for dashboard stats
    total_users = User.query.count()
    new_users_today = User.query.filter(
        User.created_at >= datetime.today().date()
    ).count()
    
    pending_kyc = KYC.query.filter_by(status='pending').count()
    open_tickets = SupportTicket.query.filter_by(status=TicketStatus.OPEN).count()
    
    recent_transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         new_users_today=new_users_today,
                         pending_kyc=pending_kyc,
                         open_tickets=open_tickets,
                         recent_transactions=recent_transactions)

 

 

@admin_bprt.route('/set-wallets', methods=['GET', 'POST'])
@login_required
def admin_set_wallets():
    session.pop('_flashes', None)

    if request.method == 'POST':
        eth_address = request.form.get('eth_address')
        btc_address = request.form.get('btc_address')
        usdt_address = request.form.get('usdt_address')
        bnb_address = request.form.get('bnb_address')

        try:
             
            eth_wallet = ETHWallet.query.first()
            if not eth_wallet:
                eth_wallet = ETHWallet()
                db.session.add(eth_wallet)
            eth_wallet.deposit = eth_address

            btc_wallet = BTCWallet.query.first()
            if not btc_wallet:
                btc_wallet = BTCWallet()
                db.session.add(btc_wallet)
            btc_wallet.deposit = btc_address

            usdt_wallet = USDTWallet.query.first()
            if not usdt_wallet:
                usdt_wallet = USDTWallet()
                db.session.add(usdt_wallet)
            usdt_wallet.deposit = usdt_address

            bnb_wallet = BNBWallet.query.first()
            if not bnb_wallet:
                bnb_wallet = BNBWallet()
                db.session.add(bnb_wallet)
            bnb_wallet.deposit= bnb_address

            db.session.commit()
            flash('Wallet addresses updated successfully!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating wallets: {str(e)}', 'danger')

        return redirect(url_for('admin.admin_set_wallets'))
 
    eth_wallet = ETHWallet.query.first()
    btc_wallet = BTCWallet.query.first()
    usdt_wallet = USDTWallet.query.first()
    bnb_wallet = BNBWallet.query.first()

    return render_template('admin/set_wallets.html', 
                           eth_wallet=eth_wallet,
                           btc_wallet=btc_wallet,
                           usdt_wallet=usdt_wallet,
                           bnb_wallet=bnb_wallet)


@admin_bprt.route('/update_balance', methods=['GET', 'POST'])
@login_required
def update_balance():
   
    if request.method == 'POST':
        session.pop('_flashes', None)
    
        email = request.form['email']
        coin = request.form['coin']
        amount = float(request.form['new_balance'])
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('admin.update_balance'))
            
        account = Account.query.filter_by(user_id=user.id).first()
        if not account:
            flash('User account not found', 'danger')
            return redirect(url_for('admin.update_balance'))
        
        # Update the appropriate coin balance
        if coin == 'BTC':
            account.BTC = amount
        elif coin == 'ETH':
            account.ETH = amount
        elif coin == 'USDT':
            account.USDT = amount
        elif coin == 'BNB':
            account.BNB = amount
            
        db.session.commit()
        flash(f"{coin} balance updated for {email}", "success")
        return redirect(url_for('admin.update_balance'))
    users= User.query.all()
    return render_template('admin/update_balance.html', users=users)

  

@admin_bprt.route('/manage-users')
@login_required
def manage_users():
    session.pop('_flashes', None)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/manage_users.html', users=users)

@admin_bprt.route('/view-user/<int:user_id>')
@login_required
def view_user(user_id):
    session.pop('_flashes', None)
    user = User.query.get_or_404(user_id)
    account = Account.query.filter_by(user_id=user_id).first()
    kyc = KYC.query.filter_by(user_id=user_id).first()
    
    return render_template('admin/view_user.html', 
                         user=user,
                         account=account,
                         kyc=kyc)

@admin_bprt.route('/update-user-balance/<int:user_id>', methods=['POST', 'GET'])
@login_required
def update_user_balance(user_id):
   
    
    if request.method == 'POST':
        session.pop('_flashes', None)
        coin = request.form['coin']
        amount = float(request.form['new_balance'])
        
        account = Account.query.filter_by(user_id=user_id).first()
        if not account:
            flash('Account not found', 'danger')
            return redirect(url_for('admin.view_user', user_id=user_id))
            
        if coin == 'BTC':
            account.BTC = amount
        elif coin == 'ETH':
            account.ETH = amount
        elif coin == 'USDT':
            account.USDT = amount
        elif coin == 'BNB':
            account.BNB = amount
            
        db.session.commit()
        flash('Balance updated successfully!', 'success')
        return redirect(url_for('admin.view_user', user_id=user_id))

@admin_bprt.route('/delete-user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    session.pop('_flashes', None)
    
    if current_user.id == user_id:
        flash('You cannot delete your own account', 'danger')
        return redirect(url_for('admin.manage_users'))
        
    user = User.query.get_or_404(user_id)
    
    # Handling support tickets before deletion
    for ticket in user.support_tickets:
        # Set the user_id to None or to a valid admin user ID (if necessary).
        ticket.user_id = None  # Or assign to admin if you want to keep the tickets
        # Alternatively, you can delete the tickets if you don't need them:
        # db.session.delete(ticket)
    
    # Handling notifications before deletion
    for notification in user.notifications:
        notification.user_id = None  # Or db.session.delete(notification)
    
    # Now delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bprt.route('/review-kyc')
@login_required
def review_kyc():
    session.pop('_flashes', None)
    pending_kycs = KYC.query.filter_by(status='pending').all()
    return render_template('admin/review_kyc.html', kyc_requests=pending_kycs)

@admin_bprt.route('/approve-kyc/<int:kyc_id>',methods=['POST', 'GET'])
@login_required
def approve_kyc(kyc_id):
    session.pop('_flashes', None)
    kyc = KYC.query.get_or_404(kyc_id)
    kyc.status = 'approved'
    kyc.reviewed_at = datetime.utcnow()
    
    # Create notification for user
    notification = Notification(
        user_id=kyc.user_id,
        title="KYC Approved",
        message="Your KYC verification has been approved",
        notification_type='success',
        link=url_for('user.kyc')
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('KYC Approved!', 'success')
    return redirect(url_for('admin.review_kyc'))

@admin_bprt.route('/reject-kyc/<int:kyc_id>', methods=['GET', 'POST'])
@login_required
def reject_kyc(kyc_id):
    session.pop('_flashes', None)
    kyc = KYC.query.get_or_404(kyc_id)
    
    if request.method == 'POST':
        notes = request.form.get('notes', '')
        kyc.status = 'rejected'
        kyc.reviewer_notes = notes
        kyc.reviewed_at = datetime.utcnow()
        
        # Create notification for user
        notification = Notification(
            user_id=kyc.user_id,
            title="KYC Rejected",
            message=f"Your KYC verification was rejected. Reason: {notes}",
            notification_type='danger',
            link=url_for('user.kyc')
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('KYC Rejected!', 'success')
        return redirect(url_for('admin.review_kyc'))
    
    return render_template('admin/reject_kyc.html', kyc=kyc)

@admin_bprt.route('/support',methods=['POST', 'GET'])
@login_required
def support_page():
    session.pop('_flashes', None)
    open_tickets = SupportTicket.query.filter(
        or_(
            SupportTicket.status == TicketStatus.OPEN,
            SupportTicket.status == TicketStatus.IN_PROGRESS
        )
    ).order_by(
        SupportTicket.created_at.desc()
    ).all()
    
    return render_template('admin/support.html', tickets=open_tickets)

@admin_bprt.route('/support/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def view_ticket(ticket_id):
    session.pop('_flashes', None)
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    if request.method == 'POST':
        message = request.form['message']
        status = request.form.get('status', ticket.status.value)
        
        # Add admin reply
        reply = TicketReply(
            ticket_id=ticket.id,
            user_id=current_user.id,
            message=message,
            is_admin_reply=True
        )
        
        # Update ticket status
        ticket.status = TicketStatus(status)
        ticket.updated_at = datetime.utcnow()
        
        # Create notification for user
        notification = Notification(
            user_id=ticket.user_id,
            title="Support Ticket Update",
            message=f"Your ticket '{ticket.subject}' has been updated",
            notification_type='info',
            link=url_for('user.view_ticket', ticket_id=ticket.id)
        )
        
        db.session.add_all([reply, notification])
        db.session.commit()
        
        flash('Reply added and ticket updated', 'success')
        return redirect(url_for('admin.view_ticket', ticket_id=ticket.id))
    
    return render_template('admin/view_ticket.html', ticket=ticket)

@admin_bprt.route('/close-ticket/<int:ticket_id>',  methods=['POST', 'GET'])
@login_required
def close_ticket(ticket_id):
    session.pop('_flashes', None)
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = TicketStatus.CLOSED
    ticket.updated_at = datetime.utcnow()
    
    # Create notification for user
    notification = Notification(
        user_id=ticket.user_id,
        title="Support Ticket Closed",
        message=f"Your ticket '{ticket.subject}' has been closed",
        notification_type='info',
        link=url_for('user.view_ticket', ticket_id=ticket.id)
    )
    
    db.session.add(notification)
    db.session.commit()
    
    flash('Ticket closed!', 'success')
    return redirect(url_for('admin.support_page'))

@admin_bprt.route('/manage-transactions',methods=['POST', 'GET'])
@login_required
def manage_transactions():
    session.pop('_flashes', None)
    transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).all()
    
    return render_template('admin/manage_transactions.html', 
                         transactions=transactions)

@admin_bprt.route('/transaction/<int:txn_id>/approve', methods=['POST', 'GET'])
@login_required
def approve_transaction(txn_id):
    session.pop('_flashes', None)
    transaction = Transaction.query.get_or_404(txn_id)
    
    if transaction.status != 'pending':
        flash('Only pending transactions can be approved', 'warning')
        return redirect(url_for('admin.manage_transactions'))
    
    # In a real app, you would implement the actual transfer logic here
    transaction.status = 'completed'
    transaction.completed_at = datetime.utcnow()
    
    # Create notification for user
    notification = Notification(
        user_id=transaction.sender_id,
        title="Transaction Approved",
        message=f"Your {transaction.coin} transaction has been processed",
        notification_type='success'
    )
    
    db.session.add(notification)
    db.session.commit()
    
    flash('Transaction approved!', 'success')
    return redirect(url_for('admin.manage_transactions'))

@admin_bprt.route('/transaction/<int:txn_id>/reject', methods=['GET', 'POST'])
@login_required
def reject_transaction(txn_id):
  
    transaction = Transaction.query.get_or_404(txn_id)
    
    if request.method == 'POST':
        session.pop('_flashes', None)
        reason = request.form['reason']
        transaction.status = 'rejected'
        transaction.completed_at = datetime.utcnow()
        
        # Create notification for user
        notification = Notification(
            user_id=transaction.sender_id,
            title="Transaction Rejected",
            message=f"Your {transaction.coin} transaction was rejected. Reason: {reason}",
            notification_type='danger'
        )
        
        db.session.add(notification)
        db.session.commit()
        
        flash('Transaction rejected!', 'success')
        return redirect(url_for('admin.manage_transactions'))
    
    return render_template('admin/reject_transaction.html', transaction=transaction)


@admin_bprt.route('/support/ticket/<int:ticket_id>/reopen', methods=['POST', 'GET'])
@login_required
def reopen_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = TicketStatus.OPEN
    db.session.commit()
    flash('Ticket reopened', 'success')
    return redirect(url_for('admin.support_page'))