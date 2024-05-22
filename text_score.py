# text_score.py

from flask import Blueprint, request, jsonify
from models import db, TextScore

text_score_bp = Blueprint('text_score', __name__)

@text_score_bp.route('/text_scores', methods=['POST'])
def add_text_score():
    data = request.json
    score = TextScore(**data)
    db.session.add(score)
    db.session.commit()
    
    return jsonify({'message': 'Text score added successfully'})

@text_score_bp.route('/text_scores', methods=['GET'])
def get_text_scores():
    scores = TextScore.query.all()
    return jsonify([s.to_dict() for s in scores])

@text_score_bp.route('/text_scores/<int:score_id>', methods=['PUT'])
def update_text_score(score_id):
    data = request.json
    score = TextScore.query.get(score_id)
    if not score:
        return jsonify({'message': 'Score not found'}), 404
    
    for key, value in data.items():
        setattr(score, key, value)
    db.session.commit()
    
    return jsonify({'message': 'Score updated successfully'})

@text_score_bp.route('/text_scores/<int:score_id>', methods=['DELETE'])
def delete_text_score(score_id):
    score = TextScore.query.get(score_id)
    if not score:
        return jsonify({'message': 'Score not found'}), 404
    
    db.session.delete(score)
    db.session.commit()
    
    return jsonify({'message': 'Score deleted successfully'})
