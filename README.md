### 📘 Simple Survey API Overview

**Project Name**: Simple Survey API  
**Base URL**: `http://<your-domain>/api`  
**Auth**: JWT Tokens

---

### 🧠 Project Purpose

This is a simple survey application which allows users to:
- Create survey questions
- Respond to survey questions
- Submit their responses (including PDF file uploads)
- View a list of all submitted responses
- Download certificates attached to a survey

---

### ⚙️ Tech Stack

- **Backend**: Python (Flask)
- **Authentication**: JWT
- **Database**: PostgreSQL
- **File Uploads**: Firebase Storage
- **ORM**: SQLAlchemy + Flask-Migrate
- **API Documentation Tool**: Postman Collection

---

### 🗃️ Database

- **DBMS**: PostgreSQL
- **Database Name**: `sky_survey_db`
- **ERD**: Located in the `/documents` folder
- **SQL Schema**: Provided in the same folder



### Project Structure
```
   simple-survey-api/
      ├── app.py
      ├── seed.py
      ├── firebase_config.py
      ├── models/
      │   ├── __init__.py
      │   ├── user.py
      │   ├── survey.py
      │   ├── submission.py
      │   ├── question.py
      │   ├── option.py
      │   ├── certificate.py
      │   └── answer.py
      ├── routes/
      │   ├── __init__.py
      │   ├── authentication.py
      │   ├── questions.py
      │   ├── survey.py
      ├── migrations/
      ├── secrets/
      │   └── jazaform_firebase_secrets.json
      ├── documents/
      │   ├── sky_survey_db_schema.sql
      │   └── erd.png
      ├── postman/
      │   └── sky_survey_api.postman_collection.json
      ├── .env
      ├── requirements.txt
      └── README.md
```


**.env Configuration:**
```
DATABASE_URL=postgresql://admin:admin@localhost:5432/sky_survey_db
SECRET_KEY=enter_your_sectret_key
JWT_SECRET_KEY=enter_your_jwt_sectret_key
FLASK_ENV=development  
```

---

### 🧩 Folder & File Purpose

| Folder/File                 | Description                        |
| --------------------------- | ---------------------------------- |
| `app.py`                    | Flask app entry point              |
| `models`                    | 
| `routes/authentication.py`  | Handles user login and auth        |
| `routes/questions.py`       | Exposes question-related endpoints |
| `routes/survey.py`          | Survey submission and processing   |
| `firebase_config.py`        | Firebase setup for file storage    |
| `seed.py`                   | Seeds database with data           |
| `secrets/*.json`            | Firebase credentials (private)     |


> ⚠️ Add Firebase credentials to the `secrets/` directory.  
> Example:

```python
cred_path = os.path.join(os.path.dirname(__file__), 'secrets', 'jazaform_firebase_secrets.json')
```

---

### 🔐 Authentication

- **Method**: JWT Token
- **Header**:
  ```
  Authorization: Bearer <your-jwt-token>
  ```

---



### 📦 Postman Collection

All API endpoints and sample responses are documented and saved in a [Postman Collection](insert-your-postman-link-here).

---

### 🛠️ Database Migrations

1. Initialize migration folder:

```bash
flask db init
```

2. Generate migration scripts:

```bash
flask db migrate -m "Initial migration."
```

3. Apply migrations:

```bash
flask db upgrade head
```

---

### 🚀 Running the Project Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/Raddames-Tonui/simple-survey-api.git
   cd simple-survey-api
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   pipenv install
   pipenv shell
   ```
3. Set environment variables via `.env` file or export manually
4. Add Firebase credentials JSON file to `secrets/` directory.
5. Run database migrations:
   ```bash
   flask db upgrade
   ```
6. Start the Flask server:
   ```bash
   flask run
   ```

---

### 📁 Related Repositories

- **Frontend (React)**: [simple-survey-client](https://github.com/Raddames-Tonui/simple-survey-client)
- **Backend (Flask API)**: [simple-survey-api](https://github.com/Raddames-Tonui/simple-survey-api)

---

### 👤 Contacts

- **GitHub**: [Raddames-Tonui](https://github.com/Raddames-Tonui)
- **LinkedIn**: [Raddames Tonui](https://www.linkedin.com/in/raddames-tonui-01a751277/)
- **Portfolio**: [My Portfolio Web](https://raddamestonui.netlify.app/)



