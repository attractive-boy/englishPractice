from flask import Blueprint, request, jsonify
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat_records', methods=['POST'])
@login_required
def create_chat_record():
    data = request.get_json()
    new_record = ChatRecord(user_id=current_user.id, question=data['question'], answer=data['answer'])
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 201

@chat_bp.route('/chat_records', methods=['GET'])
@login_required
def get_chat_records():
    records = ChatRecord.query.filter_by(user_id=current_user.id).all()
    return jsonify([record.to_dict() for record in records]), 200

@chat_bp.route('/chat_records/<int:id>', methods=['PUT'])
@login_required
def update_chat_record(id):
    record = ChatRecord.query.get_or_404(id)
    if record.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    record.question = data['question']
    record.answer = data['answer']
    db.session.commit()
    return jsonify(record.to_dict()), 200

@chat_bp.route('/chat_records/<int:id>', methods=['DELETE'])
@login_required
def delete_chat_record(id):
    record = ChatRecord.query.get_or_404(id)
    if record.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200
