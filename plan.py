from flask import Blueprint, request, jsonify
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

plan_bp = Blueprint('plan', __name__)

@plan_bp.route('/plans', methods=['POST'])
@login_required
def create_plan():
    data = request.get_json()
    new_plan = Plan(user_id=current_user.id, content=data['content'], start_date=data.get('start_date'), end_date=data.get('end_date'))
    db.session.add(new_plan)
    db.session.commit()
    return jsonify(new_plan.to_dict()), 201

@plan_bp.route('/plans', methods=['GET'])
@login_required
def get_plans():
    plans = Plan.query.filter_by(user_id=current_user.id).all()
    return jsonify([plan.to_dict() for plan in plans]), 200

@plan_bp.route('/plans/<int:id>', methods=['PUT'])
@login_required
def update_plan(id):
    plan = Plan.query.get_or_404(id)
    if plan.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    plan.content = data['content']
    plan.start_date = data.get('start_date')
    plan.end_date = data.get('end_date')
    plan.status = data.get('status', plan.status)
    plan.priority = data.get('priority', plan.priority)
    plan.is_public = data.get('is_public', plan.is_public)
    plan.category = data.get('category', plan.category)
    db.session.commit()
    return jsonify(plan.to_dict()), 200

@plan_bp.route('/plans/<int:id>', methods=['DELETE'])
@login_required
def delete_plan(id):
    plan = Plan.query.get_or_404(id)
    if plan.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200
