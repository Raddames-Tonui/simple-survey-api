from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.survey import Survey
from models.question import Question
from models.option import Option
from models.answer import Answer
from models.submission import Submission
from sqlalchemy.orm import joinedload



survey = Blueprint('survey_bp', __name__)

@survey.route('/surveys', methods=['POST'])
@jwt_required()
def create_survey():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Log the incoming data using print
    # print("Received survey data:", data)
    
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


# FETCH ALL SURVEYS FOR A USER
@survey.route('/questions/responses', methods=['GET'])
@jwt_required()
def get_user_surveys():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('page_size', 5))
    email_filter = request.args.get('email_address')

    query = Survey.query.filter_by(created_by=user_id).options(
        joinedload(Survey.submissions)
        .joinedload(Submission.answers)
        .joinedload(Answer.question),
        joinedload(Survey.submissions)
        .joinedload(Submission.certificates)
    )

    if email_filter:
        query = query.join(Survey.submissions).join(Submission.answers).join(Answer.question).filter(
            Question.name == 'email_address',
            Answer.response_value.ilike(f"%{email_filter}%")
        ).distinct()

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    survey_responses = []
    for survey in paginated.items:
        for submission in survey.submissions:
            dynamic_answers = {
                answer.question.name: answer.response_value
                for answer in submission.answers
            }

            certs = [
                {
                    'id': cert.id,
                    'file_url': cert.file_url,
                    'file_name': cert.file_name
                }
                for cert in submission.certificates
            ]

            question_response = {
                'survey_id': survey.id,
                'survey_title': survey.title,
                'response_id': submission.id,
                **dynamic_answers,
                'certificates': certs,
                'date_responded': submission.date_submitted.strftime("%Y-%m-%d %H:%M:%S")
            }

            survey_responses.append(question_response)

    return jsonify({
        "survey_responses": survey_responses,
        "current_page": paginated.page,
        "last_page": paginated.pages,
        "page_size": per_page,
        "total_count": paginated.total
    }), 200





# FECTCH QUESTIONS BASED ON SURVEY
@survey.route('/survey/<int:survey_id>/questions/', methods=['GET'])
def get_questions_by_survey(survey_id):
    # Fetch the survey by ID and check if it's published
    survey = Survey.query.filter_by(id=survey_id, is_published=True).first()
    
    if not survey:
        return jsonify({"error": "Survey not found or not published"}), 404

    # Fetch questions for this survey ordered by `order`
    questions = (
        Question.query
        .filter_by(survey_id=survey.id)
        .options(joinedload(Question.survey))
        .order_by(Question.order.asc())  
        .all()
    )

    serialized_questions = [
        {
            'question': question.serialize(),
            'survey_title': survey.title,
            'survey_description': survey.description,
            'survey_id': survey.id
        }
        for question in questions
    ]
    
    return jsonify({'questions': serialized_questions}), 200

