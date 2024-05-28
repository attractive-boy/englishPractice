from flask import Blueprint, request, jsonify
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

api_log_bp = Blueprint('api_log', __name__)

@api_log_bp.route('/api_logs', methods=['POST'])
@login_required
def create_api_log():
    data = request.get_json()
    new_log = APICallLog(user_id=current_user.id, question=data['question'], api_response=data['api_response'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify(new_log.to_dict()), 201

@api_log_bp.route('/api_logs', methods=['GET'])
@login_required
def get_api_logs():
    logs = APICallLog.query.filter_by(user_id=current_user.id).all()
    return jsonify([log.to_dict() for log in logs]), 200

@api_log_bp.route('/api_logs/<int:id>', methods=['DELETE'])
@login_required
def delete_api_log(id):
    log = APICallLog.query.get_or_404(id)
    if log.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200
