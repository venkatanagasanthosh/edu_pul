from flask import Flask, jsonify, render_template, redirect, url_for, request, session, flash
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from db import db
from datetime import datetime

print("Before importing Admin model")  # Debug statement
try:
    from models import Admin  # Assuming you have an Admin model
    print("Admin model imported successfully")  # Debug statement
except ImportError as e:
    print(f"Error importing Admin model: {e}")  # Debug statement

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    with app.app_context():
        from routes import routes_bp
        app.register_blueprint(routes_bp)
        db.create_all()  # This will create the tables based on the models

    return app

app = create_app()

@app.route('/current_date')
def current_date():
    return jsonify({'date': datetime.now().strftime('%B %d, %Y')})

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['mailid']
        password = request.form['password']
        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_admin = Admin(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        try:
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin registered successfully!', 'success')
            print("Admin registered successfully")  # Debug statement
            return redirect(url_for('admin_login'))  # Redirect to admin_login after signup
        except Exception as e:
            db.session.rollback()
            flash('Error: Could not register admin. Please try again.', 'danger')
            print(f"Error: {e}")  # Debug statement
    return render_template('Admin_Signup.html')  # Ensure this matches the template file name

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add logic to verify admin credentials
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('Admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)