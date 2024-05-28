from flask import Blueprint, request, jsonify
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports', methods=['POST'])
@login_required
def create_report():
    data = request.get_json()
    new_report = LearningReport(user_id=current_user.id, content=data['content'])
    db.session.add(new_report)
    db.session.commit()
    return jsonify(new_report.to_dict()), 201

@report_bp.route('/reports', methods=['GET'])
@login_required
def get_reports():
    reports = LearningReport.query.filter_by(user_id=current_user.id).all()
    return jsonify([report.to_dict() for report in reports]), 200

@report_bp.route('/reports/<int:id>', methods=['DELETE'])
@login_required
def delete_report(id):
    report = LearningReport.query.get_or_404(id)
    if report.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200
