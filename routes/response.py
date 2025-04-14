# import uuid
# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
# from firebase_admin import storage  
# from firebase_config import * 
# from models.submission import Submission
# from models.answer import Answer
# from models.question import Question
# from models.option import Option
# from models.certificate import Certificate
# from app import db

# response = Blueprint('response', __name__)

# # Function to upload file to Firebase Storage
# def upload_file_to_firebase(file):
#     try:
#         # Initialize Firebase storage bucket
#         bucket = storage.bucket()
#         filename = f"JazaForm/{uuid.uuid4()}_{secure_filename(file.filename)}"
#         blob = bucket.blob(filename)
        
#         print(f"Uploading file: {filename}") 
        
#         # Upload file to Firebase Storage and make it public
#         blob.upload_from_file(file, content_type=file.content_type)
#         blob.make_public()   

#         # Return the file's public URL
#         file_url = blob.public_url
#         print(f"File uploaded successfully, URL: {file_url}")
#         return file_url
#     except Exception as e:
#         print(f"Error uploading file: {str(e)}")
#         raise e  # Reraise the error for the caller to handle

# # Route to Submit Response 
# @response.route('/questions/responses', methods=["PUT"])
# def handle_survey_response():
#     try:
#         # Parse the form data and files from the request
#         data = request.form
#         files = request.files.getlist('certificates')

#         # Extract survey_id and user_id from the request
#         survey_id = data.get('survey_id')  
#         user_id = data.get('user_id')  

#         # Step 1: Create a submission entry in the database
#         submission = Submission(survey_id=survey_id, user_id=user_id)
#         db.session.add(submission)
#         db.session.flush()

#         # Step 2: Save answers to the database
#         for key in data:
#             if key.startswith('q_'):  # Assuming keys are in format 'q_<question_id>'
#                 question_id = int(key.split("_")[1])
#                 value = data[key]

#                 # Handle responses based on question type
#                 question = Question.query.get(question_id)
#                 if question.type == 'multiple_choice':
#                     answers = [v.strip() for v in value.split(",")] if "," in value else [value]
#                     for val in answers:
#                         option = Option.query.filter_by(value=val, question_id=question_id).first()
#                         db.session.add(Answer(submission_id=submission.id, question_id=question_id, option_id=option.id))
#                 else:
#                     db.session.add(Answer(submission_id=submission.id, question_id=question_id, response_value=value))

#         # Step 3: Upload certificates to Firebase Storage and save their URLs in the database
#         for file in files:
#             try:
#                 file_url = upload_file_to_firebase(file)  # Get file URL after upload
#                 # print(f"Saving certificate URL: {file_url}")
#                 # Add the URL to the Certificate model in the database
#                 certificate = Certificate(submission_id=submission.id, file_name=file.filename, file_url=file_url)
#                 db.session.add(certificate)
#             except Exception as e:
#                 print(f"Error processing file: {str(e)}")
#                 continue  # Continue processing even if one file fails


#         # Commit the transaction to save all changes
#         db.session.commit()
#         return jsonify({"message": "Response submitted successfully"}), 201

#     except Exception as e:
#         # Rollback if any error occurs
#         db.session.rollback()  
#         return jsonify({"error": str(e)}), 500


# import uuid
# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
# from firebase_admin import storage
# from firebase_config import *
# from models.submission import Submission
# from models.answer import Answer
# from models.question import Question
# from models.option import Option
# from models.certificate import Certificate
# from app import db

# response = Blueprint('response', __name__)

# # Function to upload file to Firebase Storage
# def upload_file_to_firebase(file):
#     try:
#         # Initialize Firebase storage bucket
#         bucket = storage.bucket()
#         filename = f"JazaForm/{uuid.uuid4()}_{secure_filename(file.filename)}"
#         blob = bucket.blob(filename)
        
#         print(f"Uploading file: {filename}") 
        
#         # Upload file to Firebase Storage and make it public
#         blob.upload_from_file(file, content_type=file.content_type)
#         blob.make_public()   

#         # Return the file's public URL
#         file_url = blob.public_url
#         print(f"File uploaded successfully, URL: {file_url}")
#         return file_url
#     except Exception as e:
#         print(f"Error uploading file: {str(e)}")
#         raise e  # Reraise the error for the caller to handle

# # Route to Submit Response
# @response.route('/questions/responses', methods=["PUT"])
# def handle_survey_response():
#     try:
#         # Parse the form data and files from the request
#         data = request.form
#         files = request.files.getlist('certificates')

#         # Extract survey_id and user_id from the request
#         survey_id = data.get('survey_id')  
#         user_id = data.get('user_id')  

#         # Step 1: Create a submission entry in the database
#         submission = Submission(survey_id=survey_id, user_id=user_id)
#         db.session.add(submission)
#         db.session.flush()

#         # Step 2: Save answers to the database
#         for key in data:
#             if key.startswith('q_'):  # Assuming keys are in format 'q_<question_id>'
#                 question_id = int(key.split("_")[1])
#                 value = data[key]

#                 # Handle responses based on question type
#                 question = Question.query.get(question_id)

#                 if question.type == 'multiple_choice':  # For checkboxes (multiple choice)
#                     # Check if it's a multiple selection
#                     answers = [v.strip() for v in value.split(",")] if "," in value else [value]
#                     for val in answers:
#                         option = Option.query.filter_by(value=val, question_id=question_id).first()
#                         db.session.add(Answer(submission_id=submission.id, question_id=question_id, option_id=option.id))
#                 elif question.type == 'textarea':  # For text area (text input)
#                     db.session.add(Answer(submission_id=submission.id, question_id=question_id, response_value=value))
#                 elif question.type == 'file':  # For file uploads
#                     # Files should be handled separately and uploaded to Firebase
#                     for file in files:
#                         try:
#                             file_url = upload_file_to_firebase(file)  # Get file URL after upload
#                             # Add the URL to the Certificate model in the database
#                             certificate = Certificate(submission_id=submission.id, file_name=file.filename, file_url=file_url)
#                             db.session.add(certificate)
#                         except Exception as e:
#                             print(f"Error processing file: {str(e)}")
#                             continue  # Continue processing even if one file fails
#                 else:  # For any other type, just store the value
#                     db.session.add(Answer(submission_id=submission.id, question_id=question_id, response_value=value))

#         # Step 3: Commit the transaction to save all changes
#         db.session.commit()
#         return jsonify({"message": "Response submitted successfully"}), 201

#     except Exception as e:
#         # Rollback if any error occurs
#         db.session.rollback()  
#         return jsonify({"error": str(e)}), 500

import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from firebase_admin import storage  
from firebase_config import * 
from models.submission import Submission
from models.answer import Answer
from models.question import Question
from models.option import Option
from models.certificate import Certificate
from app import db

response = Blueprint('response', __name__)

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
        raise e  # Reraise the error for the caller to handle

# Route to Submit Response 
@response.route('/questions/responses', methods=["PUT"])
def handle_survey_response():
    try:
        # Parse the form data and files from the request
        data = request.form
        files = request.files.getlist('certificates')

        # Extract survey_id and user_id from the request
        survey_id = data.get('survey_id')
        user_id = data.get('user_id')
        print("Survey ID:", survey_id)
        print("User ID:", user_id)

                
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
