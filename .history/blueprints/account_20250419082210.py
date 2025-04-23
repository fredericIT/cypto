from flask import Blueprint, redirect,url_for,render_template, request, session, flash

account_bprt= Blueprint("account",__name__, url_prefix="/account")


@account_bprt.route('/deposit')
def deposit():
    return render_template('user/deposit.html')

@account_bprt.route('/withdraw', methods=['GET', 'POST'])
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
        return redirect(url_for('account.withdraw'))

    return render_template('user/withdraw.html')