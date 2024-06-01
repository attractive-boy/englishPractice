from datetime import datetime
from flask import Blueprint, json, request, jsonify
import qianfan
from models import db
from models import User, ChatRecord, Plan, LearningReport, APICallLog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports', methods=['POST'])
@login_required
def create_report():
    data = request.get_json()
    new_report = LearningReport(
        user_id=current_user.id,
        learning_report=data['learning_report'],
        learning_suggestions=data['learning_suggestions'],
        created_at=datetime.utcnow()  # 设置当前时间
    )
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

@report_bp.route('/reports/generate', methods=['POST'])
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

        content = """请根据我和你的聊天对话，生成一个详细的学习报告和学习建议。格式如下：
        {
            "learning_report": "",
            "learning_suggestions": ""
        }
        """

        # 将历史记录转换为适合 ChatCompletion 的格式
        all_messages = [{"role": "user", "content": record.question} for record in history_records]
        all_messages.extend([{"role": "assistant", "content": record.answer} for record in history_records])
        all_messages.append({"role": "user", "content": content})

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
        return jsonify({"error": str(e)}), 500

