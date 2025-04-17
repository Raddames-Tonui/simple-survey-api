# 📘 Simple Survey API

**Project Name**: Simple Survey API  
**Base URL**: `https://simple-survey-api-fqyt.onrender.com/api`  
**Auth**: JWT Tokens

---

## 🧠 Project Purpose

This is a simple survey application that allows users to:
- Create survey questions
- Respond to survey questions
- Submit their responses (including PDF certificate uploads)
- View all submitted responses
- Download attached certificates

---

## ⚙️ Tech Stack

- **Backend**: Python (Flask)
- **Authentication**: JWT
- **Database**: PostgreSQL
- **File Uploads**: Firebase Storage
- **ORM**: SQLAlchemy + Flask-Migrate
- **API Testing**: Postman Collection

---

## 🧪 Postman Collection

All API endpoints and sample requests are available in the provided Postman collection:
- [Postman Workspace](https://dark-shuttle-668211.postman.co/workspace/My-Workspace~9d927184-69f9-4b4c-8978-451fb98f15bf/collection/40619222-4b047217-e5c4-4277-a01d-00ae2d15b976?action=share&creator=40619222)
- [Postman JSON File](./documents/simple-survey-api.postman_collection.json)

---

## 📜️ Database

- **DBMS**: PostgreSQL
- **Database Name**: `sky_survey_db`
- **ERD Diagram**: [`/documents/ERD_diagram_Simple_Survey_API.png`](./documents/ERD_diagram_Simple_Survey_API.png)
- **SQL Schema**: [`/documents/sky_survey_db_schema.sql`](./documents/sky_survey_db_schema.sql)

---

## 🔧 Project Structure
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
│   └── ERD_diagram_Simple_Survey_API.png
├── postman/
│   └── sky_survey_api.postman_collection.json
├── .env
├── requirements.txt
└── README.md
```

---

## 📄 .env Configuration
```env
DATABASE_URL=postgresql://sky_survey_db_9xg7_user:1vS6SRcrlOyChQh0v2eLJj4iTw4RFHck@dpg-cvv9bt6uk2gs73caa7ag-a.oregon-postgres.render.com/sky_survey_db_9xg7
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
FLASK_ENV=production
FIREBASE_CREDENTIALS_B64=PASTE_IT_HERE
```
> 🔐 The Firebase credentials should be stored as a Base64 string in the `.env` file and loaded inside `firebase_config.py`. To convert your Firebase JSON to Base64, run:
```bash
base64 -i secrets/jazaform_firebase_secrets.json -o encoded.txt
```
Then, copy the contents of `encoded.txt` into `FIREBASE_CREDENTIALS_B64`.

---

## 🤩️ Folder & File Purpose

| Path                           | Description                          |
|-------------------------------|--------------------------------------|
| `app.py`                      | Flask app entry point                |
| `models/`                     | Database models                      |
| `routes/authentication.py`    | User authentication logic            |
| `routes/questions.py`         | Endpoints for managing questions     |
| `routes/survey.py`           | Survey response and file uploads     |
| `firebase_config.py`          | Firebase integration for storage     |
| `seed.py`                     | Populate DB with test data           |
| `secrets/`                    | Holds Firebase credential file       |

---

## 🔐 Authentication

- **Method**: JWT
- **Header**:
  ```http
  Authorization: Bearer <your-jwt-token>
  ```

---

## 📦 Database Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🚀 Running the Project Locally

```bash
git clone https://github.com/Raddames-Tonui/simple-survey-api.git
cd simple-survey-api

# Setup and activate virtual environment
pipenv install
pipenv shell

# Add .env and Firebase credential JSON
# Run migrations
flask db upgrade

# Start the server
flask run
```

---

## 🌍 Deployment on Render

1. Push your code to GitHub:
```bash
git add .
git commit -m "deploy-ready"
git push origin main
```

2. Go to [Render](https://render.com/), create a new **Web Service**:
   - Connect to your GitHub repo
   - Set environment variables from `.env`
   - Add Build Command: `pip install -r requirements.txt`
   - Start Command: `flask run --host=0.0.0.0 --port=10000` (or use `gunicorn`)

> ✅ Make sure to include Firebase config and set the `FIREBASE_CREDENTIALS_B64` secret

---

## 📁 Related Repositories

- **Frontend (React)**: [simple-survey-client](https://github.com/Raddames-Tonui/simple-survey-client)  
  🔗 [Live Site](https://simple-survey-client-alpha.vercel.app/survey/user-surveys)

---

## 👤 Contacts

- **GitHub**: [Raddames-Tonui](https://github.com/Raddames-Tonui)
- **LinkedIn**: [Raddames Tonui](https://www.linkedin.com/in/raddames-tonui-01a751277/)
- **Portfolio**: [My Portfolio](https://raddamestonui.netlify.app/)

---


