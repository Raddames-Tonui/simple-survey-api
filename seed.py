from app import db, app
from models.survey import Survey
from models.question import Question
from models.option import Option
from models.submission import Submission
from models.answer import Answer
from models.certificate import Certificate
from models.user import User
from werkzeug.security import generate_password_hash

def seed_admin_user():
    # Create an admin user for seeding
    admin_user = User(
        email="admin@example.com",
        name="Admin User",
        role="admin"
    )
    admin_user.set_password("123") 
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created.")
    return admin_user.id  # Return the admin user ID for use in other seed functions

def seed_survey(admin_id):
    # Create a new survey for seeding
    survey = Survey(
        title="Developer Skills Survey",
        description="A survey to assess the skills of developers.",
        is_published=True,
        created_by=admin_id  # Use admin user ID as the creator
    )
    db.session.add(survey)
    db.session.commit()
    print("Survey seeded successfully.")
    return survey.id  # Return survey ID for seeding questions

def seed_questions(survey_id):
    questions_data = [
        {
            "name": "full_name", "type": "text", "required": True,
            "text": "What is your full name?", "description": "[Surname] [First Name] [Other Names]", "order": 1
        },
        {
            "name": "email_address", "type": "email", "required": True,
            "text": "What is your email address?", "description": "", "order": 2
        },
        {
            "name": "description", "type": "textarea", "required": True,
            "text": "Tell us a bit more about yourself", "description": "", "order": 3
        },
        {
            "name": "gender", "type": "radio", "required": True,
            "text": "What is your gender?", "description": "", "order": 4,
            "options": ["Male", "Female", "Other"]
        },
        {
            "name": "programming_stack", "type": "checkbox", "required": True,
            "text": "What programming stack are you familiar with?",
            "description": "You can select multiple", "order": 5,
            "options": ["React JS", "Angular JS", "Vue JS", "SQL", "Postgres", "MySQL", "MSSQL", "Java", "PHP", "Go", "Rust"]
        },
        {
            "name": "certificates", "type": "file", "required": True,
            "text": "Upload any of your certificates?", 
            "description": "You can upload multiple (.pdf)", "order": 6
        }
    ]

    for q in questions_data:
        question = Question(
            name=q["name"],
            type=q["type"],
            required=q["required"],
            text=q["text"],
            description=q["description"],
            order=q["order"], 
            survey_id=survey_id
        )
        db.session.add(question)
        db.session.flush()  # Flush to get the ID for FK use in options

        if q.get("options"):
            for opt in q["options"]:
                option = Option(value=opt, question_id=question.id)
                db.session.add(option)

    db.session.commit()
    print("Questions and options seeded successfully.")


def seed_sample_submission(survey_id, admin_id):
    # Create a sample user submission for the admin user
    submission = Submission(
        date_submitted="2023-09-21 12:30:12",
        survey_id=survey_id,
        user_id=admin_id  # Use admin user ID
    )
    db.session.add(submission)
    db.session.flush()  # Flush to get the ID

    # Sample Answers to Seed (full_name, email_address, etc.)
    answers_data = [
        {"question_name": "full_name", "response_value": "Admin User", "submission_id": submission.id},
        {"question_name": "email_address", "response_value": "admin@example.com", "submission_id": submission.id},
        {"question_name": "description", "response_value": "I am the admin user", "submission_id": submission.id},
        {"question_name": "gender", "response_value": "Male", "submission_id": submission.id},
        {"question_name": "programming_stack", "response_value": "React JS, Go", "submission_id": submission.id},
    ]

    # Add answers to the submission
    for answer_data in answers_data:
        question = Question.query.filter_by(name=answer_data["question_name"]).first()
        if question:
            answer = Answer(
                question_id=question.id,
                submission_id=answer_data["submission_id"],
                response_value=answer_data["response_value"]
            )
            db.session.add(answer)

    # Add certificates (if any)
    certificates_data = ["Admin Certificate 19-08-2023.pdf", "Admin Certification.pdf"]
    for cert_file in certificates_data:
        certificate = Certificate(submission_id=submission.id)
        certificate.save_metadata(file_url="/path/to/certificates/" + cert_file, file_name=cert_file)
        db.session.add(certificate)

    db.session.commit()
    print("Sample submission and answers seeded successfully.")

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()         # Drop all existing tables
        print("Dropping existing tables")
        db.create_all()       # Recreate all tables based on models
        print("Creating new tables")

        admin_id = seed_admin_user()
        survey_id = seed_survey(admin_id)
        seed_questions(survey_id)
        seed_sample_submission(survey_id, admin_id)
