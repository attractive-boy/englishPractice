from datetime import datetime
from flask import Blueprint, request, jsonify
import qianfan
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat_records', methods=['POST'])
@login_required
def create_chat_record():
    data = request.get_json()
    
    # 获取当天的所有聊天记录
    today = datetime.combine(datetime.today(), datetime.min.time())
    history_records = ChatRecord.query.filter(
        ChatRecord.user_id == current_user.id,
        ChatRecord.created_at >= today
    ).all()

    # 将历史记录转换为适合 ChatCompletion 的格式
    history_messages = []
    for record in history_records:
        history_messages.append({"role": "user", "content": record.question})
        history_messages.append({"role": "assistant", "content": record.answer})

    # 将当前问题添加到消息中
    current_message = {"role": "user", "content": data['question']}
    all_messages = history_messages + [current_message]

    # 调用 ChatCompletion 接口
    response = qianfan.ChatCompletion().do(
        endpoint="completions",
        temperature=0.95,
        top_p=0.8,
        penalty_score=1,
        disable_search=False,
        enable_citation=False,
        response_format="text",
        messages=all_messages
    )

    # 获取 AI 回复
    answer = response.get("result", "")

    # 创建新的聊天记录
    new_record = ChatRecord(
        user_id=current_user.id,
        question=data['question'],
        answer=answer,
        is_resolved=False  # 默认未解决
    )
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
