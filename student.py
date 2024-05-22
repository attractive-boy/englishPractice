# student.py

from flask import Blueprint, request, jsonify, session
from models import Teacher, db, Student, User
from werkzeug.security import generate_password_hash, check_password_hash

student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    student_info = {k: data.get(k) for k in ['name', 'gender', 'college', 'major', 'class_name', 'phone', 'email']}
    
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    if user_role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404

    student_info['class_name'] = teacher.class_responsible
    user = User(username=username, password=password, role='student')
    db.session.add(user)
    db.session.commit()
    
    student = Student(user_id=user.user_id, **student_info)
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'message': 'Student added successfully'})

@student_bp.route('/students', methods=['GET'])
def get_students():
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    if user_role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if teacher:
            class_name = teacher.class_responsible
            students = Student.query.filter_by(class_name=class_name).all()
        else:
            return jsonify({'error': 'Teacher not found'}), 404
    elif user_role == 'admin':
        students = Student.query.all()
    else:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify([s.to_dict() for s in students])

@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    
    return jsonify({'message': 'Student updated successfully'})

@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    db.session.delete(student)
    db.session.commit()
    
    return jsonify({'message': 'Student deleted successfully'})
