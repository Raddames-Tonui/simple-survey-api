# app.py
import os, random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Load env vars
load_dotenv()
postgres_pwd = os.getenv("DATABASE_URL")

# Setup extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Config
    # FIXED: Automatically fallback to Render DATABASE_URL if present, otherwise use local
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_pwd if postgres_pwd else "postgresql://admin:admin@localhost:5432/sky_survey_db"
    
    # FIXED: Production apps should use a stable string instead of generating random integer salts on every worker reboot (which invalidates sessions)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "$hhjd4q%h%^#7&893-fallback-salt")

    # JWT Configuration for Header-Based Auth
    app.config["JWT_TOKEN_LOCATION"] = ["headers"] 
    # FIXED: Keep the JWT key completely static so users do not get logged out randomly during Render web node recycles
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "a44u5$%*47992n3i*#*#99s29-fallback-salt")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # FIXED: Configured CORS with origin targets to answer preflight browser operations
    CORS(app, resources={
        r"/*": {
            "origins": [
                "https://vercel.app",
                "https://simple-survey-client-alpha.vercel.app",
                "http://localhost:5173"  # Local development environment route
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }, supports_credentials=True) 

    jwt = JWTManager(app)

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

    from routes.questions import questions
    from routes.authentication import auth
    from routes.survey import survey
    
    app.register_blueprint(questions, url_prefix='/api')
    app.register_blueprint(survey, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')

    return app

# Run app
app = create_app()

if __name__ == '__main__':
    if os.getenv("FLASK_ENV") == "development":
        import subprocess
        subprocess.run(["flask", "run"])
    app.run()


    
# # app.py
# import os, random
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from dotenv import load_dotenv
# from flask_jwt_extended import JWTManager
# from datetime import timedelta


# # Load env vars
# load_dotenv()
# postgres_pwd=os.getenv("DATABASE_URL")

# # Setup extensions
# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)

#     # Config
#     app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@localhost:5432/sky_survey_db"  # For developement
#     # app.config['SQLALCHEMY_DATABASE_URI'] = postgres_pwd
#     app.config["SECRET_KEY"] = "$hhjd4q%h%^#7&893" + str(random.randint(1, 1000000))

#     # JWT Configuration for Header-Based Auth
#     app.config["JWT_TOKEN_LOCATION"] = ["headers"] 
#     app.config["JWT_SECRET_KEY"] = "a44u5$%*47992n3i*#*#99s29" + str(random.randint(1, 100000))
#     app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
#     # print(os.getenv('DATABASE_URL'))

#     # Init extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     CORS(app, supports_credentials=True, ) 

#     jwt = JWTManager(app)

#     # Import models
#     from models.survey import Survey
#     from models.user import User
#     from models.answer import Answer
#     from models.certificate import Certificate
#     from models.option import Option
#     from models.question import Question
#     from models.submission import Submission

#     @app.route('/')
#     def home():
#         return "Welcome to Simple-Survey-Api!"

#     from routes.questions import questions
#     from routes.authentication import auth
#     from routes.survey import survey
    
#     app.register_blueprint(questions, url_prefix='/api')
#     app.register_blueprint(survey, url_prefix='/api')
#     app.register_blueprint(auth, url_prefix='/auth')

#     return app

# # Run app
# app = create_app()

# if __name__ == '__main__':
#     if os.getenv("FLASK_ENV") == "development":
#         import subprocess
#         subprocess.run(["flask", "run"])
#     app.run()
