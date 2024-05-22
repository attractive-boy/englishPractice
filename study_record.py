# study_record.py

from flask import Blueprint, request, jsonify
from models import db, StudentStudyRecord

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
