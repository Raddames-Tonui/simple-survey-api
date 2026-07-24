-- 1. Create USERS table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',
    date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create SURVEYS table
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_modified TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,
    CONSTRAINT fk_surveys_created_by FOREIGN KEY (created_by) 
        REFERENCES users (id) ON DELETE CASCADE
);

-- 3. Create QUESTIONS table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    required BOOLEAN NOT NULL DEFAULT TRUE,
    text VARCHAR(200) NOT NULL,
    description TEXT NULL,
    "order" INTEGER NOT NULL,
    survey_id INTEGER NOT NULL,
    CONSTRAINT fk_questions_survey_id FOREIGN KEY (survey_id) 
        REFERENCES surveys (id) ON DELETE CASCADE
);

-- 4. Create OPTIONS table
CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    value VARCHAR(255) NOT NULL,
    question_id INTEGER NOT NULL,
    CONSTRAINT fk_options_question_id FOREIGN KEY (question_id) 
        REFERENCES questions (id) ON DELETE CASCADE
);

-- 5. Create SUBMISSIONS table
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    date_submitted TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    survey_id INTEGER NOT NULL,
    user_id INTEGER NULL,
    email_address VARCHAR(255) NULL,
    CONSTRAINT fk_submissions_survey_id FOREIGN KEY (survey_id) 
        REFERENCES surveys (id) ON DELETE CASCADE,
    CONSTRAINT fk_submissions_user_id FOREIGN KEY (user_id) 
        REFERENCES users (id) ON DELETE CASCADE
);

-- 6. Create ANSWERS table
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    submission_id INTEGER NOT NULL,
    option_id INTEGER NULL,
    response_value VARCHAR(255) NULL,
    CONSTRAINT fk_answers_question_id FOREIGN KEY (question_id) 
        REFERENCES questions (id) ON DELETE CASCADE,
    CONSTRAINT fk_answers_submission_id FOREIGN KEY (submission_id) 
        REFERENCES submissions (id) ON DELETE CASCADE,
    CONSTRAINT fk_answers_option_id FOREIGN KEY (option_id) 
        REFERENCES options (id) ON DELETE SET NULL
);

-- 7. Create CERTIFICATES table
CREATE TABLE certificates (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    submission_id INTEGER NOT NULL,
    CONSTRAINT fk_certificates_submission_id FOREIGN KEY (submission_id) 
        REFERENCES submissions (id) ON DELETE CASCADE
);

-- ====================================================================
-- AUTOMATION & OPTIMIZATION ADDITIONS
-- ====================================================================

-- Trigger function to automatically maintain 'date_modified' updates
CREATE OR REPLACE FUNCTION update_date_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_modified = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_surveys_date_modified
    BEFORE UPDATE ON surveys
    FOR EACH ROW
    EXECUTE FUNCTION update_date_modified_column();

-- High-utility foreign key indexes to keep analytical queries fast
CREATE INDEX idx_surveys_created_by ON surveys(created_by);
CREATE INDEX idx_questions_survey_id ON questions(survey_id);
CREATE INDEX idx_options_question_id ON options(question_id);
CREATE INDEX idx_submissions_survey_id ON submissions(survey_id);
CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_answers_submission_id ON answers(submission_id);
CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_certificates_submission_id ON certificates(submission_id);



-- -- Users table
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(120) UNIQUE NOT NULL,
--     name VARCHAR(100) NOT NULL,
--     password_hash VARCHAR(255),
--     role VARCHAR(50) DEFAULT 'viewer' NOT NULL,
--     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Surveys table
-- CREATE TABLE surveys (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(100) NOT NULL,
--     description TEXT,
--     is_published BOOLEAN DEFAULT FALSE NOT NULL,
--     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     created_by INTEGER NOT NULL REFERENCES users(id)
-- );

-- -- Questions table
-- CREATE TABLE questions (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     type VARCHAR(50) NOT NULL,
--     required BOOLEAN DEFAULT TRUE NOT NULL,
--     text VARCHAR(200) NOT NULL,
--     description TEXT,
--     order INTEGER NOT NULL,
--     survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE
-- );

-- -- Options table
-- CREATE TABLE options (
--     id SERIAL PRIMARY KEY,
--     value VARCHAR(255) NOT NULL,
--     question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE
-- );

-- -- Submissions table
-- CREATE TABLE submissions (
--     id SERIAL PRIMARY KEY,
--     date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     survey_id INTEGER NOT NULL REFERENCES surveys(id),
--     user_id INTEGER REFERENCES users(id),
--     email_address VARCHAR(255)
-- );

-- -- Answers table
-- CREATE TABLE answers (
--     id SERIAL PRIMARY KEY,
--     question_id INTEGER NOT NULL REFERENCES questions(id),
--     submission_id INTEGER NOT NULL REFERENCES submissions(id),
--     option_id INTEGER REFERENCES options(id),
--     response_value VARCHAR(255)
-- );

-- -- Certificates table
-- CREATE TABLE certificates (
--     id SERIAL PRIMARY KEY,
--     file_url VARCHAR(255) NOT NULL,
--     file_name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE
-- );
