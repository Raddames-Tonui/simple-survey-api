
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255),
    role VARCHAR(50) DEFAULT 'viewer' NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Surveys table
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    is_published BOOLEAN DEFAULT FALSE NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL REFERENCES users(id)
);

-- Questions table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    required BOOLEAN DEFAULT TRUE NOT NULL,
    text VARCHAR(200) NOT NULL,
    description TEXT,
    order INTEGER NOT NULL,
    survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE
);

-- Options table
CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    value VARCHAR(255) NOT NULL,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE
);

-- Submissions table
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    survey_id INTEGER NOT NULL REFERENCES surveys(id),
    user_id INTEGER REFERENCES users(id),
    email_address VARCHAR(255)
);

-- Answers table
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    submission_id INTEGER NOT NULL REFERENCES submissions(id),
    option_id INTEGER REFERENCES options(id),
    response_value VARCHAR(255)
);

-- Certificates table
CREATE TABLE certificates (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE
);
