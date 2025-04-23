from flask import Blueprint, redirect,url_for,render_template, request, session, flash

users = [
        {
            'id': 1,
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'kyc_status': 'approved',
            'kyc_document': 'john_doe_id.jpg',
            'document_type': 'Passport',
            'front_image': 'john_doe_front.jpg',
            'back_image': 'john_doe_back.jpg',
            'user_with_document_image': 'john_doe_with_doc.jpg'
        },
        {
            'id': 2,
            'full_name': 'Jane Smith',
            'email': 'janesmith@example.com',
            'kyc_status': 'pending',
            'kyc_document': 'jane_smith_id.jpg',
            'document_type': 'National ID',
            'front_image': 'jane_smith_front.jpg',
            'back_image': 'jane_smith_back.jpg',
            'user_with_document_image': 'jane_smith_with_doc.jpg'
        },
        {
            'id': 3,
            'full_name': 'Alice Johnson',
            'email': 'alicejohnson@example.com',
            'kyc_status': 'rejected',
            'kyc_document': '',
            'document_type': '',
            'front_image': '',
            'back_image': '',
            'user_with_document_image': ''
        }
    ]

admin_bprt= Blueprint("admin",__name__, url_prefix="/admin")
# Admin Dashboard
# Admin Dashboard Route
@admin_bprt.route('/')
@admin_bprt.route('/dashboard')
def admin_dashboard():
    # Here you can later load stats, users count, etc.
    return render_template('admin/dashboard.html')

# Admin - Set Wallet Addresses
@admin_bprt.route('/set-wallets', methods=['GET', 'POST'])
def admin_set_wallets():
    if request.method == 'POST':
        eth_address = request.form['eth_address']
        btc_address = request.form['btc_address']
        usdt_address = request.form['usdt_address']
        bnb_address = request.form['bnb_address']

        # Save wallet addresses (for now just print, later you can save in DB or file)
        print("Wallet Addresses Updated:")
        print(f"ETH: {eth_address}")
        print(f"BTC: {btc_address}")
        print(f"USDT: {usdt_address}")
        print(f"BNB: {bnb_address}")

        # Show success message
        flash('Wallet addresses updated successfully!', 'success')
        return redirect(url_for('admin.admin_set_wallets'))

    return render_template('admin/set_wallets.html')

@admin_bprt.route('/update_balance', methods=['GET', 'POST'])
def update_balance():
    if 'user' not in session or 'admin' not in session['user']:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        email = request.form['email']
        coin = request.form['coin']
        new_balance = request.form['new_balance']

        # Here you would update the user's balance in your database
        print(f"Updating balance for {email} - {coin}: {new_balance}")

        flash(f"Balance for {email} updated successfully!", "success")
        return redirect(url_for('admin.update_balance'))

    return render_template('admin/update_balance.html')


def get_all_users():
    # Replace with actual database query to fetch all users
    return [
        {'id': 1, 'full_name': 'John Doe', 'email': 'john.doe@example.com', 'role': 'user'},
        {'id': 2, 'full_name': 'Jane Smith', 'email': 'jane.smith@example.com', 'role': 'user'},
    ]

def get_user_by_id(user_id):
    # Replace this with an actual database query to get the user by their ID
    # Example data structure for user (Replace with real data fetching)
    return {
        'id': user_id,
        'full_name': 'John Doe',
        'email': 'john.doe@example.com',
        'role': 'user',
        'wallet_address': '0xedd......ui8',  # Example wallet address
        'balances': {
            'ETH': '0.5',
            'BTC': '0.2',
            'USDT': '1000',
            'BNB': '2.5',
        }
    }


def update_user_balance_in_db(user_id, coin, new_balance):
    # Replace with actual database logic to update the user's balance
    pass

def delete_user_from_db(user_id):
    # Replace with actual database logic to delete a user
    pass


@admin_bprt.route('/manage-users')
def manage_users():
    # Fetch users from database (you will need to implement this)
    users = get_all_users()  # Example function, replace with your DB query logic.
    
    return render_template('admin/manage_users.html', users=users)
@admin_bprt.route('/view-user/<user_id>')
def view_user(user_id):
    # Fetch user details based on user_id
    user = get_user_by_id(user_id)  # Example function, replace with your DB query logic.
    
    return render_template('admin/view_user.html', user=user)

@admin_bprt.route('/update-user-balance/<user_id>', methods=['POST'])
def update_user_balance(user_id):
    if request.method == 'POST':
        coin = request.form['coin']
        new_balance = request.form['new_balance']
        
        # Update user balance logic
        update_user_balance_in_db(user_id, coin, new_balance)  # Example function, replace with your DB logic
        
        flash('Balance updated successfully!', 'success')
        return redirect(url_for('admin.view_user', user_id=user_id))

    user = get_user_by_id(user_id)
    return render_template('admin/update_user_balance.html', user=user)
@admin_bprt.route('/delete-user/<user_id>', methods=['POST'])
def delete_user(user_id):
    # Delete user from the database
    delete_user_from_db(user_id)  # Example function, replace with your DB logic
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bprt.route('/review-kyc', methods=['GET'])

def review_kyc():
    # Example static data for users and their KYC status/documents
    
    return render_template('admin/review_kyc.html', users=users)



@admin_bprt.route('/approve-kyc/<int:user_id>', methods=['GET'])
def approve_kyc(user_id):
    # Simulate approving the user's KYC status (update the KYC status)
    for user in users:
        if user['id'] == user_id:
            user['kyc_status'] = 'approved'
            break
    flash('KYC Approved!', 'success')
    return redirect(url_for('admin.review_kyc'))

@admin_bprt.route('/reject-kyc/<int:user_id>', methods=['GET'])
def reject_kyc(user_id):
    # Simulate rejecting the user's KYC status (update the KYC status)
    for user in users:
        if user['id'] == user_id:
            user['kyc_status'] = 'rejected'
            break
    flash('KYC Rejected!', 'danger')
    return redirect(url_for('admin.review_kyc'))

# Example support tickets (for testing)
tickets = [
    {
        'id': 1,
        'subject': 'Issue with Login',
        'user_email': 'user1@example.com',
        'message': 'I cannot log into my account.',
        'status': 'open'
    },
    {
        'id': 2,
        'subject': 'KYC Verification Delay',
        'user_email': 'user2@example.com',
        'message': 'My KYC is pending for a week!',
        'status': 'open'
    },
    {
        'id': 3,
        'subject': 'Feedback on Website',
        'user_email': 'user3@example.com',
        'message': 'Great website, but could be faster.',
        'status': 'closed'
    }
]

@admin_bprt.route('/support', methods=['GET'])
def support_page():
    return render_template('admin/support.html', tickets=tickets)

@admin_bprt.route('/admin/close-ticket/<int:ticket_id>', methods=['GET'])
def close_ticket(ticket_id):
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = 'closed'
            break
    flash('🎟️ Support ticket closed!', 'success')
    return redirect(url_for('admin.support_page'))


@admin_bprt.route('/manage-transactions', methods=['GET'])
def manage_transactions():
    transactions = [
        {
            'transaction_id': 'TXN123456',
            'user_fullname': 'John Doe',
            'transaction_type': 'Deposit',
            'coin': 'BTC',
            'amount': 500.00,
            'status': 'completed',
            'date': '2025-04-18 14:23'
        },
        {
            'transaction_id': 'TXN123457',
            'user_fullname': 'Jane Smith',
            'transaction_type': 'Withdrawal',
            'coin': 'BNB',
            'amount': 200.00,
            'status': 'pending',
            'date': '2025-04-18 15:45'
        },
        {
            'transaction_id': 'TXN123458',
            'user_fullname': 'Alice Johnson',
            'transaction_type': 'Deposit',
            'coin': 'ETH',
            'amount': 300.00,
            'status': 'failed',
            'date': '2025-04-17 11:00'
        }
    ]
    return render_template('admin/manage_transactions.html', transactions=transactions)