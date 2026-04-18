INSERT INTO athletes (name, age, sex, weight, height) VALUES
('Reimu Hakurei', 19, 'Female', 52.5, 164.0),
('Marisa Kirisame', 18, 'Female', 50.0, 165.0),
('Sakuya Izayoi', 18, 'Female', 51.0, 163.0),
('Youmu Konpaku', 16, 'Female', 48.5, 160.0),
('Houraisan Kaguya', 17, 'Female', 53.0, 167.0),
('Cirno', 9, 'Female', 30.0, 130.0),
('Alice Margatroid', 16, 'Female', 49.0, 162.0),
('Patchouli Knowledge', 16, 'Female', 45.0, 157.0),
('Remilia Scarlet', 495, 'Female', 42.0, 137.0),
('Flandre Scarlet', 495, 'Female', 40.0, 135.0);

INSERT INTO nutrition_logs (athlete_id, meal_type, calories, protein, carbs, fats, log_date) VALUES
(1, 'breakfast', 450, 20, 55, 15, '2026-04-17'),
(2, 'lunch', 700, 35, 80, 25, '2026-04-17'),
(3, 'dinner', 650, 30, 70, 20, '2026-04-17'),
(4, 'breakfast', 500, 25, 60, 18, '2026-04-17'),
(5, 'lunch', 720, 40, 85, 22, '2026-04-17'),
(6, 'snack', 200, 5, 30, 8, '2026-04-17'),
(7, 'breakfast', 480, 22, 58, 16, '2026-04-17'),
(8, 'lunch', 600, 18, 75, 20, '2026-04-17'),
(9, 'dinner', 800, 28, 90, 30, '2026-04-17'),
(10, 'snack', 180, 4, 25, 7, '2026-04-17');

INSERT INTO training_sessions (athlete_id, session_type, duration_minutes, intensity, calories_burned, session_date) VALUES
(1, 'cardio', 45, 'Medium', 320, '2026-04-17'),
(2, 'strength', 60, 'High', 500, '2026-04-17'),
(3, 'fencing', 50, 'High', 450, '2026-04-17'),
(4, 'combat training', 40, 'High', 420, '2026-04-17'),
(5, 'wind magic training', 55, 'Medium', 380, '2026-04-17'),
(6, 'flight practice', 30, 'Low', 150, '2026-04-17'),
(7, 'puppet control training', 60, 'Medium', 300, '2026-04-17'),
(8, 'spellcasting endurance', 70, 'Low', 200, '2026-04-17'),
(9, 'vampire agility drills', 35, 'High', 600, '2026-04-17'),
(10, 'destruction control practice', 30, 'Low', 650, '2026-04-17');

INSERT INTO recovery_logs (athlete_id, sleep_hours, soreness_level, stress_level, recovery_score, log_date) VALUES
(1, 6.5, 5, 6, 70, '2026-04-17'),
(2, 7.0, 4, 5, 75, '2026-04-17'),
(3, 6.0, 6, 7, 68, '2026-04-17'),
(4, 5.5, 7, 6, 60, '2026-04-17'),
(5, 7.5, 3, 4, 80, '2026-04-17'),
(6, 9.0, 1, 2, 95, '2026-04-17'),
(7, 6.8, 4, 5, 72, '2026-04-17'),
(8, 8.0, 2, 3, 88, '2026-04-17'),
(9, 5.0, 8, 6, 55, '2026-04-17'),
(10, 5.0, 9, 7, 50, '2026-04-17');

INSERT INTO goals (athlete_id, goal_type, target_value, current_value, start_date, end_date) VALUES
(1, 'endurance', 100.0, 62.0, '2026-01-01', '2026-06-01'),
(2, 'strength', 120.0, 85.0, '2026-01-01', '2026-06-01'),
(3, 'agility', 90.0, 70.0, '2026-01-01', '2026-06-01'),
(4, 'combat skill', 95.0, 78.0, '2026-01-01', '2026-06-01'),
(5, 'magic control', 100.0, 88.0, '2026-01-01', '2026-06-01'),
(6, 'flight speed', 80.0, 60.0, '2026-01-01', '2026-06-01'),
(7, 'precision', 90.0, 75.0, '2026-01-01', '2026-06-01'),
(8, 'mana efficiency', 100.0, 90.0, '2026-01-01', '2026-06-01'),
(9, 'agility', 110.0, 95.0, '2026-01-01', '2026-06-01'),
(10, 'destruction control', 100.0, 92.0, '2026-01-01', '2026-06-01');