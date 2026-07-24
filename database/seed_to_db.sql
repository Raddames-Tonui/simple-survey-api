-- Wrap everything in a single transaction block to guarantee isolation
BEGIN;

-- 1. SEED ADMINISTRATIVE USER
-- Replicates seed_admin_user()
-- Password hash value is an explicit conversion of string "123"
INSERT INTO users (id, email, name, password_hash, role, date_created)
VALUES (
    1, 
    'admin@example.com', 
    'Admin User', 
    'scrypt:32768:16:1$hUqH6xRkK0g0p89J$dbb99bb6368d40a2334e2c60fbc8c86bc9cd2f65a1215b1fb443eb54fa16b0dfa1f81d45903bda9e17fe89f7fb093e8787f08c3aef542cf95dd26b9a8976b052', 
    'creator', 
    CURRENT_TIMESTAMP
);

-- 2. SEED THE BASE SURVEY
-- Replicates seed_survey(admin_id)
INSERT INTO surveys (id, title, description, is_published, created_by)
VALUES (
    1, 
    'Developer Skills Survey', 
    'A survey to assess the skills of developers.', 
    TRUE, 
    1
);

-- 3. SEED SURVEY QUESTIONS
-- Replicates seed_questions(survey_id)
INSERT INTO questions (id, name, type, required, text, description, "order", survey_id) VALUES
(1, 'full_name', 'text', TRUE, 'What is your full name?', '[Surname] [First Name] [Other Names]', 1, 1),
(2, 'email_address', 'email', TRUE, 'What is your email address?', '', 2, 1),
(3, 'description', 'textarea', TRUE, 'Tell us a bit more about yourself', '', 3, 1),
(4, 'gender', 'radio', TRUE, 'What is your gender?', '', 4, 1),
(5, 'programming_stack', 'checkbox', TRUE, 'What programming stack are you familiar with?', 'You can select multiple', 5, 1),
(6, 'certificates', 'file', TRUE, 'Upload any of your certificates?', 'You can upload multiple (.pdf)', 6, 1);

-- 4. SEED STATIC SELECTABLE OPTIONS
-- Replicates options assignment loop within seed_questions()
INSERT INTO options (id, value, question_id) VALUES
(1, 'Male', 4),
(2, 'Female', 4),
(3, 'Other', 4),
(4, 'React JS', 5),
(5, 'Angular JS', 5),
(6, 'Vue JS', 5),
(7, 'SQL', 5),
(8, 'Postgres', 5),
(9, 'MySQL', 5),
(10, 'MSSQL', 5),
(11, 'Java', 5),
(12, 'PHP', 5),
(13, 'Go', 5),
(14, 'Rust', 5);

-- 5. SEED INITIAL SAMPLE ADMIN SUBMISSION
-- Replicates seed_sample_submission(survey_id, admin_id)
INSERT INTO submissions (id, date_submitted, survey_id, user_id, email_address)
VALUES (1, '2023-09-21 12:30:12'::timestamp, 1, 1, 'admin@example.com');

-- 6. SEED INITIAL ANSWERS AND METADATA CERTIFICATES FOR ADMIN SUBMISSION
INSERT INTO answers (question_id, submission_id, response_value) VALUES
(1, 1, 'Admin User'),
(2, 1, 'admin@example.com'),
(3, 1, 'I am the admin user'),
(4, 1, 'Male'),
(5, 1, 'React JS, Go');

INSERT INTO certificates (file_url, file_name, submission_id) VALUES
('/path/to/certificates/Admin Certificate 19-08-2023.pdf', 'Admin Certificate 19-08-2023.pdf', 1),
('/path/to/certificates/Admin Certification.pdf', 'Admin Certification.pdf', 1);


-- 7. GENERATE 40 RANDOMIZED BULK TEST SUBMISSIONS
-- Replicates seed_multiple_submissions(survey_id) using standard Postgres mathematical random matrices
DO $$
DECLARE
    new_sub_id INT;
    f_name TEXT;
    l_name TEXT;
    full_name TEXT;
    email_addr TEXT;
    rand_gender TEXT;
    rand_stack TEXT;
    rand_date TIMESTAMP;
    first_cert_file TEXT;
    second_cert_file TEXT;
    
    -- Immutable data matrices matching python definitions
    first_names TEXT[] := ARRAY['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Jamie', 'Sam', 'Chris', 'Pat', 'Terry', 'Robin', 'Dana', 'Kelly', 'Shannon', 'Jesse'];
    last_names TEXT[] := ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson'];
    genders TEXT[] := ARRAY['Male', 'Female', 'Other'];
    techs TEXT[] := ARRAY['React JS', 'Angular JS', 'Vue JS', 'SQL', 'Postgres', 'MySQL', 'MSSQL', 'Java', 'PHP', 'Go', 'Rust'];
    tech_count INT;
    chosen_techs TEXT[];
BEGIN
    FOR i IN 2..41 LOOP
        -- Generate mock credentials pseudo-randomly
        f_name := first_names[floor(random() * array_length(first_names, 1) + 1)];
        l_name := last_names[floor(random() * array_length(last_names, 1) + 1)];
        full_name := f_name || ' ' || l_name;
        email_addr := lower(f_name) || '.' || lower(l_name) || i || '@example.net';
        rand_gender := genders[floor(random() * array_length(genders, 1) + 1)];
        
        -- Create a dynamic variable timeline window spanning backward exactly 365 days
        rand_date := CURRENT_TIMESTAMP - (random() * INTERVAL '365 days');
        
        -- Shuffle elements cleanly to generate a multi-selected comma array list for the checkbox model
        tech_count := floor(random() * 4 + 2)::INT; -- Picks between 2 and 5 items
        chosen_techs := ARRAY[]::TEXT[];
        WHILE array_length(chosen_techs, 1) IS NULL OR array_length(chosen_techs, 1) < tech_count LOOP
            DECLARE
                selected_tech TEXT := techs[floor(random() * array_length(techs, 1) + 1)];
            BEGIN
                IF NOT (chosen_techs @> ARRAY[selected_tech]) THEN
                    chosen_techs := array_append(chosen_techs, selected_tech);
                END IF;
            END;
        END LOOP;
        rand_stack := array_to_string(chosen_techs, ', ');

        -- Persist main submission tracking metric
        INSERT INTO submissions (id, date_submitted, survey_id, user_id, email_address)
        VALUES (i, rand_date, 1, NULL, email_addr)
        RETURNING id INTO new_sub_id;

        -- Persist atomic response details mapping across generated ids
        INSERT INTO answers (question_id, submission_id, response_value) VALUES
        (1, new_sub_id, full_name),
        (2, new_sub_id, email_addr),
        (3, new_sub_id, 'This is a bulk programmatic response simulating developer skills experience profiles for ' || full_name || '.'),
        (4, new_sub_id, rand_gender),
        (5, new_sub_id, rand_stack);

        -- Persist mock certificate structure records (randomly assigns 1 or 2 items)
        first_cert_file := replace(full_name, ' ', '_') || '_Cert_0.pdf';
        INSERT INTO certificates (file_url, file_name, submission_id, created_at)
        VALUES ('/fake/path/' || first_cert_file, first_cert_file, new_sub_id, rand_date);
        
        IF random() > 0.5 THEN
            second_cert_file := replace(full_name, ' ', '_') || '_Cert_1.pdf';
            INSERT INTO certificates (file_url, file_name, submission_id, created_at)
            VALUES ('/fake/path/' || second_cert_file, second_cert_file, new_sub_id, rand_date);
        END IF;

    END LOOP;
END $$;

-- 8. ALIGN SERIAL SEQUENCE COUNTERS FOR INDEPENDENT PRIMARY KEYS
-- Prevents key duplication errors on future manual web client submissions
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('surveys_id_seq', (SELECT MAX(id) FROM surveys));
SELECT setval('questions_id_seq', (SELECT MAX(id) FROM questions));
SELECT setval('options_id_seq', (SELECT MAX(id) FROM options));
SELECT setval('submissions_id_seq', (SELECT MAX(id) FROM submissions));

COMMIT;
