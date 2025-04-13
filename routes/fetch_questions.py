from flask import Blueprint, request, jsonify, send_file
from app import db
from models import Question,  Certificate
from models.survey import Survey
from sqlalchemy.orm import joinedload
from firebase_admin import storage

questions = Blueprint('questions', __name__)

# FETCH ALL QUESTIONS
@questions.route('/questions', methods=['GET'])
def get_questions():
    # Fetch all questions along with their associated survey
    questions = Question.query.options(joinedload(Question.survey)).all()
    
    # Serialize the survey title and description along with the questions
    serialized_questions = [
        {
            'question': question.serialize(),
            'survey_title': question.survey.title,
            'survey_description': question.survey.description,
            'survey_id': question.survey.id
        }
        for question in questions
    ]

    return jsonify({'questions': serialized_questions}), 200


#  FETCH ALL SURVEYS
@questions.route('/surveys', methods=['GET'])
def get_all_surveys():
    surveys = Survey.query.all()

    if not surveys:
        return jsonify({"message": "No surveys found."}), 404

    serialized_surveys = [survey.serialize() for survey in surveys]

    return jsonify({"surveys" : serialized_surveys}), 200

# FECTCH QUESTIONS BASED ON SURVEY
@questions.route('/questions/<int:survey_id>', methods=['GET'])
def get_questions_by_survey(survey_id):
    # Fetch the survey by ID and check if it's published
    survey = Survey.query.filter_by(id=survey_id, is_published=True).first()
    
    if not survey:
        return jsonify({"error": "Survey not found or not published"}), 404

    # Fetch questions related to the specified published survey ID
    questions = Question.query.filter_by(survey_id=survey.id).options(joinedload(Question.survey)).all()

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



  

# Download certificate by ID
@questions.route('/questions/responses/certificates/<int:cert_id>', methods=['GET'])
def download_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    return send_file(cert.file_url, as_attachment=True)
