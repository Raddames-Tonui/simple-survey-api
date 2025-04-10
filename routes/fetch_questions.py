from flask import Blueprint, request, jsonify, send_file
from app import db
from models import Question,  Certificate
from sqlalchemy.orm import joinedload
from firebase_admin import storage

questions = Blueprint('questions', __name__)

# Fetch list of questions
@questions.route('/questions', methods=['GET'])
def get_questions():
    # Fetch all questions along with their associated survey
    questions = Question.query.options(joinedload(Question.survey)).all()
    
    # Serialize the survey title and description along with the questions
    serialized_questions = [
        {
            'question': question.serialize(),
            'survey_title': question.survey.title,
            'survey_description': question.survey.description
        }
        for question in questions
    ]

    return jsonify({'questions': serialized_questions}), 200

  

# Download certificate by ID
@questions.route('/questions/responses/certificates/<int:cert_id>', methods=['GET'])
def download_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    return send_file(cert.file_url, as_attachment=True)
