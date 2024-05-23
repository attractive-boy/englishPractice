from flask import Blueprint, request, jsonify, session
from models import db, StudentStudyRecord
from datetime import datetime, timedelta

from spark_ai import get_scores_from_spark_api

study_record_bp = Blueprint('study_record', __name__)

@study_record_bp.route('/study_records', methods=['POST'])
def add_study_record():
    data = request.json
    record = StudentStudyRecord(**data)
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'message': 'Study record added successfully'})

@study_record_bp.route('/study_records', methods=['GET'])
def get_study_records():
    records = StudentStudyRecord.query.all()
    return jsonify([r.to_dict() for r in records])

@study_record_bp.route('/study_records/weekly', methods=['GET'])
def get_weekly_study_records():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    end_date = datetime.utcnow().date() - timedelta(days=1)  # 计算到昨天为止
    start_date = end_date - timedelta(days=6)  # 从昨天往前推7天

    study_records = StudentStudyRecord.query.filter(
        StudentStudyRecord.student_id == user_id,
        StudentStudyRecord.study_date.between(start_date, end_date)
    ).all()

    updated_records = []
    for record in study_records:
        needs_update = not all([
            record.lexical_difficulty_score,
            record.syntactic_complexity_score,
            record.readability_formula_score,
            record.text_structure_score,
            record.reader_background_knowledge_score
        ])
        
        if needs_update:
            # Call Spark API to get scores
            conversations = [
                {"role": "user", "content": record.content},  # 假设 content 包含对话文本
                # 可以继续添加对话内容
            ]
            scores = get_scores_from_spark_api(conversations)
            record.lexical_difficulty_score = scores['lexical_difficulty_score']
            record.syntactic_complexity_score = scores['syntactic_complexity_score']
            record.readability_formula_score = scores['readability_formula_score']
            record.text_structure_score = scores['text_structure_score']
            record.reader_background_knowledge_score = scores['reader_background_knowledge_score']
            db.session.commit()
            updated_records.append(record)

    return jsonify({
        'records': [r.to_dict() for r in study_records],
        'updated_records': [r.to_dict() for r in updated_records]
    })

@study_record_bp.route('/study_records/<int:record_id>', methods=['PUT'])
def update_study_record(record_id):
    data = request.json
    record = StudentStudyRecord.query.get(record_id)
    if not record:
        return jsonify({'message': 'Record not found'}), 404
    
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    
    return jsonify({'message': 'Record updated successfully'})

@study_record_bp.route('/study_records/<int:record_id>', methods=['DELETE'])
def delete_study_record(record_id):
    record = StudentStudyRecord.query.get(record_id)
    if not record:
        return jsonify({'message': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'message': 'Record deleted successfully'})