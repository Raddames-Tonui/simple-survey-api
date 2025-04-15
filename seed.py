from app import db, app
from models.survey import Survey
from models.question import Question
from models.option import Option
from models.submission import Submission
from models.answer import Answer
from models.certificate import Certificate
from models.user import User
from faker import Faker
from werkzeug.security import generate_password_hash
import random

fake = Faker()

def seed_admin_user():
    admin_user = User(
        email="admin@example.com",
        name="Admin User",
        role="creator"
    )
    admin_user.set_password("123")
    db.session.add(admin_user)
    db.session.commit()
    print("First user created successfully.")
    return admin_user.id

def seed_survey(admin_id):
    survey = Survey(
        title="Developer Skills Survey",
        description="A survey to assess the skills of developers.",
        is_published=True,
        created_by=admin_id
    )
    db.session.add(survey)
    db.session.commit()
    print("Survey seeded successfully.")
    return survey.id

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
        db.session.flush()

        if q.get("options"):
            for opt in q["options"]:
                option = Option(value=opt, question_id=question.id)
                db.session.add(option)

    db.session.commit()
    print("Questions and options seeded successfully.")

def seed_sample_submission(survey_id, admin_id):
    submission = Submission(
        date_submitted="2023-09-21 12:30:12",
        survey_id=survey_id,
        user_id=admin_id,
        email_address="admin@example.com"
    )
    db.session.add(submission)
    db.session.flush()

    answers_data = [
        {"question_name": "full_name", "response_value": "Admin User", "submission_id": submission.id},
        {"question_name": "email_address", "response_value": "admin@example.com", "submission_id": submission.id},
        {"question_name": "description", "response_value": "I am the admin user", "submission_id": submission.id},
        {"question_name": "gender", "response_value": "Male", "submission_id": submission.id},
        {"question_name": "programming_stack", "response_value": "React JS, Go", "submission_id": submission.id},
    ]

    for answer_data in answers_data:
        question = Question.query.filter_by(name=answer_data["question_name"]).first()
        if question:
            answer = Answer(
                question_id=question.id,
                submission_id=answer_data["submission_id"],
                response_value=answer_data["response_value"]
            )
            db.session.add(answer)

    certificates_data = ["Admin Certificate 19-08-2023.pdf", "Admin Certification.pdf"]
    for cert_file in certificates_data:
        certificate = Certificate(submission_id=submission.id)
        certificate.save_metadata(file_url="/path/to/certificates/" + cert_file, file_name=cert_file)
        db.session.add(certificate)

    db.session.commit()
    print("Sample submission and answers seeded successfully.")

def seed_multiple_submissions(survey_id):
    questions = Question.query.filter_by(survey_id=survey_id).all()
    question_map = {q.name: q for q in questions}
    
    tech_stacks = ["React JS", "Angular JS", "Vue JS", "SQL", "Postgres", "MySQL", "MSSQL", "Java", "PHP", "Go", "Rust"]
    genders = ["Male", "Female", "Other"]

    for _ in range(40):
        email = fake.email()
        full_name = fake.name()
        submission = Submission(
            survey_id=survey_id,
            email_address=email,
            date_submitted=fake.date_time_between(start_date='-1y', end_date='now')
        )
        db.session.add(submission)
        db.session.flush()

        answers = [
            Answer(
                question_id=question_map["full_name"].id,
                submission_id=submission.id,
                response_value=full_name
            ),
            Answer(
                question_id=question_map["email_address"].id,
                submission_id=submission.id,
                response_value=email
            ),
            Answer(
                question_id=question_map["description"].id,
                submission_id=submission.id,
                response_value=fake.text(max_nb_chars=200)
            ),
            Answer(
                question_id=question_map["gender"].id,
                submission_id=submission.id,
                response_value=random.choice(genders)
            ),
            Answer(
                question_id=question_map["programming_stack"].id,
                submission_id=submission.id,
                response_value=", ".join(random.sample(tech_stacks, k=random.randint(2, 5)))
            ),
        ]

        db.session.add_all(answers)

        for i in range(random.randint(1, 2)):
            cert_file = f"{full_name.replace(' ', '_')}_Cert_{i}.pdf"
            cert = Certificate(submission_id=submission.id)
            cert.save_metadata(file_url=f"/fake/path/{cert_file}", file_name=cert_file)
            db.session.add(cert)

    db.session.commit()
    print("40 random submissions seeded successfully.")

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        print("Dropping existing tables")
        db.create_all()
        print("Creating new tables")

        admin_id = seed_admin_user()
        survey_id = seed_survey(admin_id)
        seed_questions(survey_id)
        seed_sample_submission(survey_id, admin_id)
        seed_multiple_submissions(survey_id)
