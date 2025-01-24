from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import Student

# Create a Blueprint for routes
routes_bp = Blueprint('routes', __name__)

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
        if student.email == data['username']:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid username'}), 401
    return jsonify({'message': 'Invalid credentials'}), 401

@routes_bp.route('/check_db', methods=['GET'])
def check_db():
    try:
        # Attempt to query the database
        student_count = Student.query.count()
        return jsonify({'message': 'Database connection successful', 'student_count': student_count}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500
