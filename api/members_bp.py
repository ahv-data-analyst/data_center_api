from flask import Blueprint, g, jsonify, request
from json import loads
from models.records import MembershipRecord, AssessmentRecord

members_bp = Blueprint("members", __name__)

@members_bp.route("/")
def get_members():
    data = g.db_manager.members.fetch_all()
    result = []
    for i in data:
        result.append(loads(i.to_json()))
        
    return jsonify(result), 200

@members_bp.route('/add', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        member_data = MembershipRecord(
            id=0,
            assessment_date=data['assessment_date'],
            trsh_membership_number=data['membership_number'],
            assessment_code=data['assessment_code'],
            name=data['name'],
            surname=data['surname'],
            serving_group=data['serving_group'],
            cell_number=data['cell_number'],
            birth_of_date=data['date_of_birth'],
            province=data['province'],
            country_of_attendance=data['country'],
            branch=data['branch'],
            year_of_arrival=data['year_of_arrival'],
            gender=data['gender'],
        )
        
        ass_count = g.db_manager.assessments.get_count()
        
        assessment_data = AssessmentRecord(
            assessment_id= f"ass-{ass_count + 1}",
            name=data['name'],
            surname=data['surname'],
            membership_number=data['membership_number'],
            assessment_code=data['assessment_code'],
            assessment_result=0,
            interview_result='PENDING',
            assessment_date=data['assessment_date'],
            serving_group=data['serving_group'],
        )
        assessment_data.add_interview_result()
        assessment_data.add_pass_fail()
        assessment_data.add_unique_code()
        
        g.db_manager.members.insert(member_data)
        g.db_manager.assessments.insert(assessment_data)
        
        return jsonify({
            'message': 'Member added successfully',
            'added_to_king': True,
        }), 201
        
    except Exception as e:
        print(e.with_traceback())
        return jsonify({'error': str(e)}), 500

@members_bp.route("/pagmembers", methods=['GET'])
def get_page_members():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    group = request.args.get('group', None)
    
    total_count, data = g.db_manager.members.fetch_page(page, limit, group)
    
    result = []
    for i in data:
        result.append(loads(i.to_json()))
    
    return jsonify({
        "total": total_count,
        "page": page,
        "limit": limit,
        "data": result
    }), 200