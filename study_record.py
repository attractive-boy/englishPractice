from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, session
from models import ChatMessage, Student, Teacher, User, db, StudentStudyRecord
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

    # 获取可选的 student_id 参数
    student_id = request.args.get('student_id')

    # 如果未提供 student_id 参数，则使用当前会话中的 user_id
    if not student_id or student_id == 'undefined':
        # Fetch the student_id using user_id
        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        student_id = student.student_id
    else:
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

    end_date = datetime.utcnow().date() - timedelta(days=1)  # Calculate up to yesterday
    start_date = end_date - timedelta(days=6)  # From yesterday back 7 days

    study_records = StudentStudyRecord.query.filter(
        StudentStudyRecord.student_id == student_id,
        StudentStudyRecord.study_date.between(start_date, end_date)
    ).all()

    # Create a dictionary to store the records by date
    records_dict = {record.study_date: record for record in study_records}

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
            start_of_day = datetime.combine(record.study_date, datetime.min.time())
            end_of_day = datetime.combine(record.study_date, datetime.max.time())

            previous_messages = ChatMessage.query.filter(
                ChatMessage.user_id == user_id,
                ChatMessage.timestamp.between(start_of_day, end_of_day)
            ).order_by(ChatMessage.timestamp).all()
            conversations = [{"role": "user", "content": msg.content} for msg in previous_messages]
            scores = get_scores_from_spark_api(conversations)
            record.lexical_difficulty_score = scores['lexical_difficulty_score']
            record.syntactic_complexity_score = scores['syntactic_complexity_score']
            record.readability_formula_score = scores['readability_formula_score']
            record.text_structure_score = scores['text_structure_score']
            record.reader_background_knowledge_score = scores['reader_background_knowledge_score']
            record.score = sum(scores.values())

            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                return jsonify({'error': 'Database update failed', 'details': str(e)}), 500

    # Ensure every day in the past 7 days has a record
    complete_records = []
    for single_date in (start_date + timedelta(n) for n in range(7)):
        if single_date in records_dict:
            complete_records.append(records_dict[single_date])
        else:
            # Create a default record for missing dates
            default_record = StudentStudyRecord(
                student_id=student_id,
                study_date=single_date,
                lexical_difficulty_score=0,
                syntactic_complexity_score=0,
                readability_formula_score=0,
                text_structure_score=0,
                reader_background_knowledge_score=0,
                score=0
            )
            complete_records.append(default_record)

    return jsonify({
        'records': [record.to_dict() for record in complete_records]
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

@study_record_bp.route('/study_records/weekly/average', methods=['GET'])
def get_weekly_average_study_records():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(user_id)  # 假设有一个 User 模型表示用户信息

    if user.role == 'teacher':
        # 假设 Teacher 模型有一个 class_id 表示老师的班级
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404
        students = Student.query.filter_by(class_name=teacher.class_responsible).all()
    else:
        students = Student.query.all()

    end_date = datetime.utcnow().date() - timedelta(days=1)  # Calculate up to yesterday
    start_date = end_date - timedelta(days=6)  # From yesterday back 7 days

    result = []

    for student in students:
        study_records = StudentStudyRecord.query.filter(
            StudentStudyRecord.student_id == student.student_id,
            StudentStudyRecord.study_date.between(start_date, end_date)
        ).all()

        if not study_records:
            continue

        total_scores = {
            'lexical_difficulty_score': 0,
            'syntactic_complexity_score': 0,
            'readability_formula_score': 0,
            'text_structure_score': 0,
            'reader_background_knowledge_score': 0,
            'score': 0,
            'duration_minutes': 0,
            'count': 0,
            'scenarios': {}
        }

        for record in study_records:
            total_scores['lexical_difficulty_score'] += record.lexical_difficulty_score
            total_scores['syntactic_complexity_score'] += record.syntactic_complexity_score
            total_scores['readability_formula_score'] += record.readability_formula_score
            total_scores['text_structure_score'] += record.text_structure_score
            total_scores['reader_background_knowledge_score'] += record.reader_background_knowledge_score
            total_scores['score'] += record.score
            total_scores['duration_minutes'] += record.duration_minutes
            total_scores['count'] += 1
            
            scenario = record.scenario.name
            if scenario not in total_scores['scenarios']:
                total_scores['scenarios'][scenario] = 0
            total_scores['scenarios'][scenario] += 1

        if total_scores['count'] > 0:
            most_common_scenario = max(total_scores['scenarios'], key=total_scores['scenarios'].get)
            average_scores = {
                'student_id': student.student_id,
                'average_lexical_difficulty_score': total_scores['lexical_difficulty_score'] / total_scores['count'],
                'average_syntactic_complexity_score': total_scores['syntactic_complexity_score'] / total_scores['count'],
                'average_readability_formula_score': total_scores['readability_formula_score'] / total_scores['count'],
                'average_text_structure_score': total_scores['text_structure_score'] / total_scores['count'],
                'average_reader_background_knowledge_score': total_scores['reader_background_knowledge_score'] / total_scores['count'],
                'average_score': total_scores['score'] / total_scores['count'],
                'average_duration_minutes': total_scores['duration_minutes'] / total_scores['count'],
                'most_common_scenario': most_common_scenario
            }
            result.append(average_scores)

    return jsonify(result)