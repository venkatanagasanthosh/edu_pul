import random
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import Admin, Student

routes_bp = Blueprint('routes', __name__)
admin_bp = Blueprint('admin', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/studentlogin')
def student_login():
    return render_template('studentlogin.html')

@routes_bp.route('/studentsignup')
def student_signup():
    return render_template('student_signup.html')

@routes_bp.route('/signup', methods=['POST'])
def signup():
    data = request.form
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_student = Student(
        first_name=data['first_name'],
        middle_name=data.get('middle_name'),
        last_name=data['last_name'],
        phone_number=data['phone_number'],
        email=data['email'],
        branch=data['branch'],
        password=hashed_password
    )
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('routes.signup_success'))

@routes_bp.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')

@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    student = Student.query.filter_by(email=data['email']).first()
    if student and check_password_hash(student.password, data['password']):
        session['student_id'] = student.id
        session['student_first_name'] = student.first_name
        return redirect(url_for('routes.student_dashboard'))
    return jsonify({'message': 'Invalid credentials'}), 401

@routes_bp.route('/student_dashboard')
def student_dashboard():
    first_name = session.get('student_first_name', 'Student')
    return render_template('Studentdashboard.html', first_name=first_name)

@routes_bp.route('/check_db', methods=['GET'])
def check_db():
    try:
        student_count = Student.query.count()
        return jsonify({'message': 'Database connection successful', 'student_count': student_count}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500

@routes_bp.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@routes_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.form
    student = Student.query.filter_by(email=data['email'], phone_number=data['phone_number']).first()
    if student:
        hashed_password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
        student.password = hashed_password
        db.session.commit()
        return redirect(url_for('routes.student_login'))
    return jsonify({'message': 'Invalid email or phone number'}), 401

@admin_bp.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('mailid')
        password = request.form.get('password')

        print(f"Received data: {first_name}, {last_name}, {email}, {password}")  # Debug statement

        if not first_name or not last_name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.admin_signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            new_admin = Admin(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin registered successfully!', 'success')
            print("Admin registered successfully")  # Debug statement
            return redirect(url_for('admin.admin_login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving admin: {e}', 'danger')
            print(f"Error: {e}")  # Debug statement
            return redirect(url_for('admin.admin_signup'))

    return render_template('Admin_Signup.html')

@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password, password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            flash('Login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('admin_login.html')

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    return render_template('Admin_dashboard.html')
