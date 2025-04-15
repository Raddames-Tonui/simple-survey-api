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

import uuid, requests
from werkzeug.utils import secure_filename
from collections import defaultdict


from io import BytesIO


questions = Blueprint('questions', __name__)


# ============================================================================================================================

# a) FETCH ALL QUESTIONS
@questions.route('/questions', methods=['GET'])
def get_all_questions_grouped_by_survey():
    # Fetch all questions, along with their associated survey and options
    all_questions = Question.query.options(
        joinedload(Question.survey),  
        joinedload(Question.options) 
    ).all()

    # Use defaultdict to group questions under their respective surveys
    # The lambda function sets up the default structure for each survey group
    grouped = defaultdict(lambda: {
        'id': None,
        'title': '',
        'description': '',
        'questions': []
    })

    for q in all_questions:
        survey_id = q.survey.id
        
        # Set survey metadata only once for each group
        grouped[survey_id]['id'] = survey_id
        grouped[survey_id]['title'] = q.survey.title
        grouped[survey_id]['description'] = q.survey.description

        # Append the serialized question to the corresponding survey group
        grouped[survey_id]['questions'].append(q.serialize())

    # Convert defaultdict to a list of grouped survey-question objects
    return jsonify(list(grouped.values())), 200


# b) FETCH QUESTIONS OF A PARTICULAR SURVEY
@questions.route('/questions/survey/<int:survey_id>', methods=['GET'])
def get_questions_of_a_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({'error': 'Survey not found'}), 404
    
    survey_data = survey.serialize()
    survey_data['questions'] = [q.serialize() for q in survey.questions]

    return jsonify(survey_data), 200


# ============================================================================================================================

# c) ROUTE TO SUBMIT RESPONSE
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
        email_address = data.get('email')
        # print("Survey ID:", survey_id "User ID:", user_id)
       
                
        # If user_id is not provided, set it to None
        user_id = user_id if user_id else None

        # Step 1: Create a submission entry in the database
        submission = Submission(survey_id=survey_id, user_id=user_id, email_address=email_address)
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

# d) FETCH ALL SURVEY QUESTIONS WITH ANSWERS FOR A USER
@questions.route('/questions/responses', methods=['GET'])
@jwt_required()
def get_user_surveys_answers():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('page_size', 5))
    email_filter = request.args.get('email_address')

    # Base query on submissions created by the current user's surveys
    query = Submission.query.join(Submission.survey).filter(Survey.created_by == user_id).options(
        joinedload(Submission.survey),
        joinedload(Submission.answers).joinedload(Answer.question),
        joinedload(Submission.certificates)
    )

    # Apply email filter directly on the email_address field
    if email_filter:
        query = query.filter(Submission.email_address.ilike(f"%{email_filter}%"))

    # Pagination
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    survey_responses = []
    for submission in paginated.items:
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
            'survey_id': submission.survey.id,
            'survey_title': submission.survey.title,
            'response_id': submission.id,
            **dynamic_answers,
            'email_address': submission.email_address,
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



# ============================================================================================================================

# e) DOWNLOAD CERTIFICATE 
@questions.route('/questions/responses/certificates/<int:cert_id>', methods=['GET'])
def stream_certificate(cert_id):
    certificate = Certificate.query.get(cert_id)
    if not certificate:
        return jsonify({"message": "Certificate not found"}), 404

    response = requests.get(certificate.file_url)
    if response.status_code != 200:
        return jsonify({"message": "Failed to download file from Firebase"}), 500

    return send_file(
        BytesIO(response.content),
        download_name=certificate.file_name,
        as_attachment=True
    )



@questions.route('/surveys/user-surveys', methods=['GET'])
@jwt_required()
def get_user_surveys():
    user_id = get_jwt_identity()

    surveys = Survey.query.filter_by(created_by=user_id).all()

    if not surveys:
        return jsonify({"message": "No surveys found for this user."}), 404

    return jsonify({"surveys": [s.serialize() for s in surveys]}), 200

