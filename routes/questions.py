from flask import Blueprint, request, jsonify, send_file
from app import db

from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.survey import Survey
from models.question import Question
from models.answer import Answer
from models.submission import Submission
from models.option import Option
from models.certificate import  Certificate
from models.survey import Survey
from models.user import User

from firebase_config import * 
from firebase_admin import storage  

import uuid
from werkzeug.utils import secure_filename

questions = Blueprint('questions', __name__)

# ============================================================================================================================

# a) FETCH ALL QUESTIONS
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


# ============================================================================================================================

# b) ROUTE TO SUBMIT RESPONSE
# Function to upload file to Firebase Storage
def upload_file_to_firebase(file):
    try:
        # Initialize Firebase storage bucket
        bucket = storage.bucket()
        filename = f"JazaForm/{uuid.uuid4()}_{secure_filename(file.filename)}"
        blob = bucket.blob(filename)
        
        # print(f"Uploading file: {filename}") 
        
        # Upload file to Firebase Storage and make it public
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()   

        # Return the file's public URL
        file_url = blob.public_url
        # print(f"File uploaded successfully, URL: {file_url}")
        return file_url
    except Exception as e:
        # print(f"Error uploading file: {str(e)}")
        raise e 
    
 
# ROUTE TO SUBMIT RESPONSE
@questions.route('/questions/responses', methods=["PUT"])
def handle_survey_response():
    try:
        # Parse the form data and files from the request
        data = request.form
        files = request.files.getlist('certificates')

        # Extract survey_id and user_id from the request
        survey_id = data.get('survey_id')
        user_id = data.get('user_id')
        # print("Survey ID:", survey_id)
        # print("User ID:", user_id)

                
        # If user_id is not provided, set it to None
        user_id = user_id if user_id else None

        # Step 1: Create a submission entry in the database
        submission = Submission(survey_id=survey_id, user_id=user_id)
        db.session.add(submission)
        db.session.flush()  # Get submission.id without committing yet

        # Step 2: Save answers to the database
        for key in data:
            if key.startswith('q_'):  # Format: q_<question_id>
                try:
                    question_id = int(key.split("_")[1])
                    value = data[key]

                    question = Question.query.get(question_id)
                    if not question:
                        continue  # Skip invalid question_id

                    if question.type == 'multiple_choice':
                        answers = [v.strip() for v in value.split(",")] if "," in value else [value]
                        for val in answers:
                            option = Option.query.filter_by(value=val, question_id=question_id).first()
                            if option:
                                db.session.add(Answer(
                                    submission_id=submission.id,
                                    question_id=question_id,
                                    option_id=option.id
                                ))
                    else:
                        db.session.add(Answer(
                            submission_id=submission.id,
                            question_id=question_id,
                            response_value=value
                        ))
                except Exception as e:
                    continue  # Skip bad question formats

        # Step 3: Upload certificates to Firebase and save URLs
        for file in files:
            try:
                file_url = upload_file_to_firebase(file)
                certificate = Certificate(
                    submission_id=submission.id,
                    file_name=file.filename,
                    file_url=file_url
                )
                db.session.add(certificate)
            except Exception as e:
                continue  # Skip individual file failures

        # Finalize transaction
        db.session.commit()
        return jsonify({"message": "Response submitted successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================================================================================

# c) FETCH ALL SURVEY QUESTIONS WITH ANSWERS FOR A USER
@questions.route('/questions/responses', methods=['GET'])
@jwt_required()
def get_user_surveys_answers():
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

    # Apply email filter only to answers to the email address question
    if email_filter:
        query = query.join(Survey.submissions).join(Submission.answers).join(Answer.question).filter(
            Question.name == 'email_address',  # Targeting the 'email_address' question
            Answer.response_value.ilike(f"%{email_filter}%")  # Filtering the email
        )

    # Pagination
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
    })


