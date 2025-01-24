from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import Student

# Create a Blueprint for routes
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
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
    return jsonify({'message': 'Student registered successfully'}), 201

@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    student = Student.query.filter_by(email=data['email']).first()
    if student and check_password_hash(student.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
