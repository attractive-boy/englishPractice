# scenario.py

from flask import Blueprint, request, jsonify
from models import db, Scenario

scenario_bp = Blueprint('scenario', __name__)

@scenario_bp.route('/scenarios', methods=['POST'])
def add_scenario():
    data = request.json
    scenario = Scenario(**data)
    db.session.add(scenario)
    db.session.commit()
    
    return jsonify({'message': 'Scenario added successfully'})

@scenario_bp.route('/scenarios', methods=['GET'])
def get_scenarios():
    scenarios = Scenario.query.all()
    return jsonify([s.to_dict() for s in scenarios])

@scenario_bp.route('/scenarios/<int:scenario_id>', methods=['PUT'])
def update_scenario(scenario_id):
    data = request.json
    scenario = Scenario.query.get(scenario_id)
    if not scenario:
        return jsonify({'message': 'Scenario not found'}), 404
    
    for key, value in data.items():
        setattr(scenario, key, value)
    db.session.commit()
    
    return jsonify({'message': 'Scenario updated successfully'})

@scenario_bp.route('/scenarios/<int:scenario_id>', methods=['DELETE'])
def delete_scenario(scenario_id):
    scenario = Scenario.query.get(scenario_id)
    if not scenario:
        return jsonify({'message': 'Scenario not found'}), 404
    
    db.session.delete(scenario)
    db.session.commit()
    
    return jsonify({'message': 'Scenario deleted successfully'})
