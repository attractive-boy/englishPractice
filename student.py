from flask import Blueprint, request, jsonify, session
from models import Teacher, db, Student, User
from werkzeug.security import generate_password_hash, check_password_hash

student_bp = Blueprint('student', __name__)

@student_bp.route('/students/profile', methods=['GET'])
def get_student_profile():
    user_id = session.get('user_id')
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict())

@student_bp.route('/students/profile', methods=['PUT'])
def update_student_profile():
    user_id = session.get('user_id')
    data = request.json
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@student_bp.route('/students/password', methods=['PUT'])
def update_student_password():
    user_id = session.get('user_id')
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'})
