# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Setup extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import models
    from models.survey import Survey
    from models.user import User
    from models.answer import Answer
    from models.certificate import Certificate
    from models.option import Option
    from models.question import Question
    from models.submission import Submission

    @app.route('/')
    def home():
        return "Welcome to Simple-Survey-Api!"

    # Import routes     
    from routes.fetch_questions import questions
    from routes.response import response
    from routes.fetch_responses import answers
    from routes.download_certificates import certificates
    app.register_blueprint(questions, url_prefix='/api')
    app.register_blueprint(response, url_prefix='/api')
    app.register_blueprint(answers, url_prefix='/api')
    app.register_blueprint(certificates, url_prefix='/api')

    return app

# Run app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
