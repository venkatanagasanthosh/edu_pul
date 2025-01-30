from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_migrate import Migrate
from config import Config
from db import db
from models import CGPA, Parent, Student, Attendance  # Ensure these models are defined to interact with the respective tables

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    from routes import routes_bp, admin_bp
    from my_dashboard import my_dashboard_bp  # Ensure this is imported as a Blueprint
    app.register_blueprint(routes_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(my_dashboard_bp, url_prefix='/dashboard')

    @app.route('/parent/signup', methods=['POST'])
    def parent_signup():
        data = request.json
        student_id = data.get('student_id')
        face_id = data.get('face_id')

        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return jsonify({'error': 'Student ID not found'}), 404

        new_parent = Parent(student_id=student_id, face_id=face_id)
        db.session.add(new_parent)
        db.session.commit()

        return jsonify({'message': 'Parent signed up successfully'})

    @app.route('/parent/login', methods=['POST'])
    def parent_login():
        data = request.json
        face_id = data.get('face_id')

        parent = Parent.query.filter_by(face_id=face_id).first()
        if not parent:
            return jsonify({'error': 'Face ID not recognized'}), 401

        student = Student.query.filter_by(id=parent.student_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        cgpa_data = CGPA.query.filter_by(student_id=student.id).all()
        attendance_data = Attendance.query.filter_by(student_id=student.id).all()

        cgpa_list = [{'semester': cgpa.semester, 'cgpa': cgpa.cgpa} for cgpa in cgpa_data]
        attendance_list = [{'date': att.date, 'status': att.status} for att in attendance_data]

        return redirect(url_for('parent_dashboard'))

    @app.route('/parent/dashboard')
    def parent_dashboard():
        return render_template('parent_dashboard.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
