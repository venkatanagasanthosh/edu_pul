from db import db
import numpy as np

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)  # First Name
    last_name = db.Column(db.String(100), nullable=False)   # Last Name
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Admin {self.email}>'

class CGPA(db.Model):
    __tablename__ = 'cgpa'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)

    student = db.relationship('Student', backref=db.backref('cgpas', lazy=True))

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    percentage = db.Column(db.Float, nullable=False)

    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))

class Parent(db.Model):
    __tablename__ = "parent"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    face_encoding = db.Column(db.LargeBinary, nullable=False)  # Store face encoding

    student = db.relationship("Student", backref=db.backref("parents", lazy=True))

    def set_face_encoding(self, encoding):
        """Convert numpy array encoding to binary"""
        self.face_encoding = encoding.tobytes()

    def get_face_encoding(self):
        """Retrieve binary face encoding and convert to numpy array"""
        return np.frombuffer(self.face_encoding, dtype=np.float64)

