from flask import Blueprint, g, jsonify, request
from json import loads

assessment_bp = Blueprint("assessment", __name__)

@assessment_bp.route("/number")
def search_by_number():
    number = request.args.get('number', None, type=str)
    data = g.db_manager.assessments.fetch(number)
    
    result = []
    for i in data:
        result.append(loads(i.to_json()))
        
    return jsonify(result)

@assessment_bp.route('/<string:number>', methods=['PATCH'])
def upate_results(number: str):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
    
        record = g.db_manager.assessments.fetch(number)[0]
        
        if not record:
            return jsonify({'error': 'User not found'}), 404
    
        ass_results = data['assessment_results']
        int_results = data['interview_results']
        
        if ass_results != "":
            record.assessment_result = ass_results
            record.add_pass_fail()
            
        if int_results != "":
            record.interview_result = int_results
            
        g.db_manager.assessments.update_assessment_results(number, record)
        
        return jsonify({
            'message': 'Results successfully updated',
        }), 200
    except Exception as e:
        print(e.with_traceback())
        return jsonify({'error': str(e)}), 500

@assessment_bp.route("/assessments")
def get_assessments():
    data = g.db_manager.assessments.fetch_all()
    
    result = []
    for i in data:
        result.append(loads(i.to_json()))
        
    return jsonify(result)

@assessment_bp.route("/pagassessments")
def get_page():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    group = request.args.get('group', None)
    
    total_count, data = g.db_manager.assessments.fetch_page(page, limit, group)
    
    result = []
    for i in data:
        result.append(loads(i.to_json()))
        
    return jsonify({
        "total": total_count,
        "page": page,
        "limit": limit,
        "data": result
    }), 200