# teacher.py

from flask import Blueprint, request, jsonify, session
from models import db, Teacher, User
from werkzeug.security import generate_password_hash, check_password_hash

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teachers', methods=['POST'])
def add_teacher():
    data = request.json
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    teacher_info = {k: data.get(k) for k in ['name', 'gender', 'college', 'teacher_number', 'phone', 'email', 'class_responsible']}
    
    user = User(username=username, password=password, role='teacher')
    db.session.add(user)
    db.session.commit()
    
    teacher = Teacher(user_id=user.user_id, **teacher_info)
    db.session.add(teacher)
    db.session.commit()
    
    return jsonify({'message': 'Teacher added successfully'})

@teacher_bp.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers])

@teacher_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    data = request.json
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    
    for key, value in data.items():
        setattr(teacher, key, value)
    db.session.commit()
    
    return jsonify({'message': 'Teacher updated successfully'})

@teacher_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    
    db.session.delete(teacher)
    db.session.commit()
    
    return jsonify({'message': 'Teacher deleted successfully'})

@teacher_bp.route('/teachers/password', methods=['PUT'])
def update_password():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user or not check_password_hash(user.password, current_password):
        return jsonify({'message': '当前密码错误'}), 400
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'message': '密码更新成功'})

# 获取教师个人信息
@teacher_bp.route('/teachers/profile', methods=['GET'])
def get_teacher_profile():
    user_id = session.get('user_id')
    teacher = Teacher.query.filter_by(user_id=user_id).first()
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404
    return jsonify(teacher.to_dict())

# 更新教师个人信息
@teacher_bp.route('/teachers/profile', methods=['PUT'])
def update_teacher_profile():
    data = request.json
    user_id = session.get('user_id')
    teacher = Teacher.query.filter_by(user_id=user_id).first()
    if not teacher:
        return jsonify({'message': 'Teacher not found'}), 404

    for key, value in data.items():
        setattr(teacher, key, value)
    db.session.commit()
    
    return jsonify({'message': 'Profile updated successfully'})
