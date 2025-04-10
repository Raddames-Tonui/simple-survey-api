from flask import Blueprint, request, jsonify
from app import db
from models import Submission, Answer, Question
from sqlalchemy.orm import joinedload
from datetime import datetime

answers = Blueprint('answers', __name__)

# Fetch submitted responses
@answers.route('/questions/responses', methods=['GET'])
def get_responses():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('page_size', 10))
    email_filter = request.args.get('email_address')

    query = Submission.query.options(
        joinedload(Submission.answers).joinedload(Answer.question),
        joinedload(Submission.certificates)
    )

    if email_filter:
        query = query.join(Submission.answers).join(Answer.question).filter(
            Question.name == 'email_address',
            Answer.response_value.ilike(f"%{email_filter}%")
        )

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    question_responses = []
    for submission in paginated.items:
        # Dynamically extract answers
        dynamic_answers = {
            answer.question.name: answer.response_value
            for answer in submission.answers
        }

        # Prepare certificates
        certs = [
            {
                'id': cert.id,
                'file_url': cert.file_url,
                'file_name': cert.file_name
            }
            for cert in submission.certificates
        ]

        # Build the full response object
        question_response = {
            'response_id': submission.id,
            **dynamic_answers,  # spread all dynamic fields
            'certificates': certs,
            'date_responded': submission.date_submitted.strftime("%Y-%m-%d %H:%M:%S")
        }

        question_responses.append(question_response)

    return jsonify({
        "question_responses": question_responses,
        "current_page": paginated.page,
        "last_page": paginated.pages,
        "page_size": per_page,
        "total_count": paginated.total
    }), 200
