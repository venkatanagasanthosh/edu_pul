from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from routes import *
        db.create_all()

    return app

app = create_app()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/signup', methods=['POST'])
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    student = Student.query.filter_by(email=data['email']).first()
    if student and check_password_hash(student.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
