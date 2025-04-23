from dotenv import load_dotenv
load_dotenv()
from flask import Flask, flash, render_template, request, redirect, url_for, session
from alchemy import db
import os

app = Flask(__name__)
app.config.from_object("config.Config")
# initialize the app with the extension
db.init_app(app)

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


# Home redirects to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        withdraw_password = request.form['withdraw_password']

        # Save to database (we will add db later)
        print(f"Registered: {full_name}, {email}")

        return "Registered successfully! (This is a temporary message)"
    
    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user (database logic will be added later)
        print(f"Login attempt: {email}")

        # Simulate login success
        session['user'] = email

        if 'admin' in email.lower():
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')


# Dashboard page (after login)
@app.route('/dashboard')
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
        return redirect(url_for('login'))

    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/trade')
def trade():
    return render_template('user/trade.html')


@app.route('/user/deposit')
def deposit():
    return render_template('user/deposit.html')

@app.route('/user/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        # Get form data
        withdraw_address = request.form['withdraw_address']
        coin = request.form['coin']
        amount = float(request.form['amount'])
        withdraw_password = request.form['withdraw_password']

        # Here you can add your logic: check balance, validate password, etc.
        
        # Simulate saving withdrawal request...
        # After everything is OK:

        flash('✅ Withdrawal request submitted successfully!', 'success')
        return redirect(url_for('withdraw'))

    return render_template('user/withdraw.html')

@app.route('/transaction_history')
def transactions():
    # Example transactions (later you will load from database)
    transactions = [
        {"type": "Deposit", "coin": "BTC", "amount": "0.005", "status": "Completed", "date": "2025-04-17"},
        {"type": "Withdraw", "coin": "ETH", "amount": "0.2", "status": "Pending", "date": "2025-04-16"},
        {"type": "Trade Profit", "coin": "USDT", "amount": "12", "status": "Completed", "date": "2025-04-15"},
    ]
    return render_template('user/transaction_history.html', transactions=transactions)


@app.route('/profile')
def profile():
    return render_template('user/profile.html')

@app.route('/user/kyc', methods=['GET', 'POST'])
def kyc():
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

@app.route('/user/notifications')
def notifications():
    # Example notification data
    notifications = [
        {"title": "KYC Approved ✅", "message": "Your identity verification has been approved.", "date": "2025-04-17", "type": "success"},
        {"title": "Withdrawal Request Sent 💸", "message": "We received your withdrawal request.", "date": "2025-04-16", "type": "info"},
    ]
    return render_template('user/notifications.html', notifications=notifications)
@app.route('/user/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']

        # You can save the ticket to database or email it to admin

        flash('✅ Your support request has been submitted!', 'success')
        return redirect(url_for('support'))

    return render_template('user/support.html')







# Admin Dashboard
# Admin Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    # Here you can later load stats, users count, etc.
    return render_template('admin/dashboard.html')

# Admin - Set Wallet Addresses
@app.route('/admin/set-wallets', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_set_wallets'))

    return render_template('admin/set_wallets.html')

@app.route('/admin/update_balance', methods=['GET', 'POST'])
def update_balance():
    if 'user' not in session or 'admin' not in session['user']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']
        coin = request.form['coin']
        new_balance = request.form['new_balance']

        # Here you would update the user's balance in your database
        print(f"Updating balance for {email} - {coin}: {new_balance}")

        flash(f"Balance for {email} updated successfully!", "success")
        return redirect(url_for('update_balance'))

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


@app.route('/admin/manage-users')
def manage_users():
    # Fetch users from database (you will need to implement this)
    users = get_all_users()  # Example function, replace with your DB query logic.
    
    return render_template('admin/manage_users.html', users=users)
@app.route('/admin/view-user/<user_id>')
def view_user(user_id):
    # Fetch user details based on user_id
    user = get_user_by_id(user_id)  # Example function, replace with your DB query logic.
    
    return render_template('admin/view_user.html', user=user)

@app.route('/admin/update-user-balance/<user_id>', methods=['POST'])
def update_user_balance(user_id):
    if request.method == 'POST':
        coin = request.form['coin']
        new_balance = request.form['new_balance']
        
        # Update user balance logic
        update_user_balance_in_db(user_id, coin, new_balance)  # Example function, replace with your DB logic
        
        flash('Balance updated successfully!', 'success')
        return redirect(url_for('view_user', user_id=user_id))

    user = get_user_by_id(user_id)
    return render_template('admin/update_user_balance.html', user=user)
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
def delete_user(user_id):
    # Delete user from the database
    delete_user_from_db(user_id)  # Example function, replace with your DB logic
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/review-kyc', methods=['GET'])

def review_kyc():
    # Example static data for users and their KYC status/documents
    
    return render_template('admin/review_kyc.html', users=users)



@app.route('/admin/approve-kyc/<int:user_id>', methods=['GET'])
def approve_kyc(user_id):
    # Simulate approving the user's KYC status (update the KYC status)
    for user in users:
        if user['id'] == user_id:
            user['kyc_status'] = 'approved'
            break
    flash('KYC Approved!', 'success')
    return redirect(url_for('review_kyc'))

@app.route('/admin/reject-kyc/<int:user_id>', methods=['GET'])
def reject_kyc(user_id):
    # Simulate rejecting the user's KYC status (update the KYC status)
    for user in users:
        if user['id'] == user_id:
            user['kyc_status'] = 'rejected'
            break
    flash('KYC Rejected!', 'danger')
    return redirect(url_for('review_kyc'))

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

@app.route('/admin/support', methods=['GET'])
def support_page():
    return render_template('admin/support.html', tickets=tickets)

@app.route('/admin/close-ticket/<int:ticket_id>', methods=['GET'])
def close_ticket(ticket_id):
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = 'closed'
            break
    flash('🎟️ Support ticket closed!', 'success')
    return redirect(url_for('support_page'))


@app.route('/admin/manage-transactions', methods=['GET'])
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



if __name__ == '__main__':
    
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
