from flask import Blueprint, json, request, jsonify
import qianfan
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

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

@plan_bp.route('/plans/generate', methods=['POST'])
@login_required
def generate_plan():
    try:
        # 获取当天的所有聊天记录
        today = datetime.combine(datetime.today(), datetime.min.time())
        history_records = ChatRecord.query.filter(
            ChatRecord.user_id == current_user.id,
            ChatRecord.created_at >= today
        ).all()
        if not history_records:
            return jsonify({'message': 'No chat history found'}), 404
        content = """请根据我和你的聊天对话，严格按照以下格式生成一个基于数据结构课程详细的学习计划,只返回JSON字符串不要有多余的内容：
                    {
                        "content": "",
                        "start_date": "",
                        "end_date": "",
                        "status": "",
                        "priority": ,
                        "is_public": ,
                        "category": ""
                    }
                  """
        # 将历史记录转换为适合 ChatCompletion 的格式
        all_messages = []
        for record in history_records:
            all_messages.append({"role": "user", "content": record.question})
            all_messages.append({"role": "assistant", "content": record.answer})
        current_message = {"role": "user", "content": content}
        all_messages = all_messages + [current_message]

        response = qianfan.ChatCompletion().do(
            endpoint="completions",
            temperature=0.95,
            top_p=0.8,
            penalty_score=1,
            disable_search=False,
            enable_citation=False,
            response_format="text",
            messages=all_messages,
        )

        raw_string = response.get("result", "")
        # 移除前面的无用部分
        cleaned_string = raw_string.split('```json', 1)[-1].strip().rstrip('```').strip()

        # 将清理后的字符串转换为 Python 字典
        data = json.loads(cleaned_string)

        # 将 Python 字典转换为格式化的 JSON 字符串
        formatted_json = json.dumps(data, ensure_ascii=False, indent=4)

        return formatted_json, 201
    except Exception as e:
        return jsonify({"error": e}), 500
