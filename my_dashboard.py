from flask import Blueprint, jsonify
from db import db

my_dashboard_bp = Blueprint('my_dashboard', __name__)

@my_dashboard_bp.route('/api/attendance')
def get_attendance():
    # Fetch attendance data from the database
    attendance_data = {
        'present': 50,
        'absent': 10,
        'late': 5
    }
    return jsonify(attendance_data)
