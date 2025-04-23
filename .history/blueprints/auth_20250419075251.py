from flask import Blueprint, redirect,url_for,render_template, request, session

auth_bprt= Blueprint("auth",__name__, url_prefix="/auth")


@auth_bprt.route("/", methods=["GET", "POST"])
def auth():
   return redirect(url_for('auth.login'))

@auth_bprt.route("/login", methods=["GET","POST"])
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

@auth_bprt.route("/register",methods=["GET","POST"])
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