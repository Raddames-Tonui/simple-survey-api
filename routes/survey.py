from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.survey import Survey
from models.question import Question
from models.option import Option
from models.answer import Answer
from models.submission import Submission
from models.user import User
from sqlalchemy.orm import joinedload

survey = Blueprint('survey_bp', __name__)

# CREATE A SURVEY
@survey.route('/surveys/create', methods=['POST'])
@jwt_required()
def create_survey():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Log the incoming data using print
    print("Received survey data:", data)
    
    # Or, using logging:
    
    try:
        # Validate required survey fields
        title = data.get('title')
        description = data.get('description', '')
        is_published = data.get('is_published', False)
        questions_data = data.get('questions', [])

        if not title:
            return jsonify({"error": "Survey title is required"}), 400

        if not isinstance(questions_data, list) or not questions_data:
            return jsonify({"error": "At least one question is required"}), 400

        # Create Survey
        survey_obj = Survey(
            title=title,
            description=description,
            is_published=is_published,
            created_by=user_id
        )
        db.session.add(survey_obj)
        db.session.flush()

        for q in questions_data:
            # Validate presence of required fields
            required_fields = ['name', 'text', 'type', 'order']
            missing_fields = [field for field in required_fields if field not in q]
            empty_fields = [field for field in ['name', 'text', 'type'] if not q.get(field)]

            if missing_fields or empty_fields:
                return jsonify({
                    "error": f"Missing required question fields: {missing_fields + empty_fields}"
                }), 400

            question_type = q['type']
            options = q.get('options', [])

            # Only allow options for specific types
            if question_type not in ['radio', 'checkbox']:
                options = []

            question_obj = Question(
                name=q['name'],
                type=question_type,
                required=q.get('required', False),
                text=q['text'],
                description=q.get('description', ''),
                order=q['order'],
                survey_id=survey_obj.id
            )
            db.session.add(question_obj)
            db.session.flush()

            # Add options if valid
            for opt_value in options:
                if isinstance(opt_value, str) and opt_value.strip():
                    option_obj = Option(
                        value=opt_value.strip(),
                        question_id=question_obj.id
                    )
                    db.session.add(option_obj)

        db.session.commit()
        return jsonify({
            "message": "Survey created successfully",
            "survey_id": survey_obj.id
        }), 201

    except Exception as e:
        db.session.rollback()
        print("Error in create_survey:", str(e))
        return jsonify({"error": str(e)}), 500




#  FETCH ALL SURVEYS
@survey.route('/surveys', methods=['GET'])
def get_all_surveys():
    surveys = Survey.query.all()

    if not surveys:
        return jsonify({"message": "No surveys found."}), 404

    serialized_surveys = [survey.serialize() for survey in surveys]

    return jsonify({"surveys" : serialized_surveys}), 200


# FETCH SURVEYS OF AUTHENTICATED USER
@survey.route('/surveys/user-surveys', methods=['GET'])
@jwt_required()
def get_user_surveys():
    user_id = get_jwt_identity()

    surveys = Survey.query.filter_by(created_by=user_id).all()

    if not surveys:
        return jsonify({"message": "No surveys found for this user."}), 404

    return jsonify({"surveys": [s.serialize() for s in surveys]}), 200

