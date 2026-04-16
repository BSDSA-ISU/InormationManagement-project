CREATE DATABASE athlete_dashboard;
USE athlete_dashboard;

CREATE TABLE athletes (
    athlete_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    sex ENUM('Male', 'Female', 'Other'),
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nutrition_logs (
    nutrition_id INT AUTO_INCREMENT PRIMARY KEY,
    athlete_id INT NOT NULL,
    meal_type VARCHAR(50), -- breakfast, lunch, etc.
    calories INT NOT NULL,
    protein DECIMAL(5,2),
    carbs DECIMAL(5,2),
    fats DECIMAL(5,2),
    log_date DATE NOT NULL,

    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
        ON DELETE CASCADE
);

CREATE TABLE training_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    athlete_id INT NOT NULL,
    session_type VARCHAR(50), -- cardio, strength, etc.
    duration_minutes INT NOT NULL,
    intensity ENUM('Low', 'Medium', 'High'),
    calories_burned INT,
    session_date DATE NOT NULL,

    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
        ON DELETE CASCADE
);

CREATE TABLE recovery_logs (
    recovery_id INT AUTO_INCREMENT PRIMARY KEY,
    athlete_id INT NOT NULL,
    sleep_hours DECIMAL(3,1),
    soreness_level INT, -- 1–10 scale
    stress_level INT,   -- optional but nice
    recovery_score INT, -- derived or manual
    log_date DATE NOT NULL,

    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
        ON DELETE CASCADE
);

CREATE TABLE goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    athlete_id INT NOT NULL,
    goal_type VARCHAR(50), -- weight loss, endurance, etc.
    target_value DECIMAL(6,2),
    current_value DECIMAL(6,2),
    start_date DATE,
    end_date DATE,

    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
        ON DELETE CASCADE
);

