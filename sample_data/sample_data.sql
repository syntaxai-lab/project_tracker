INSERT INTO projects (name, description, start_date, end_date, status)
VALUES 
('AI Tracker', 'Tracking AI development tasks', '2025-08-01', '2025-09-01', 'active'),
('Web Revamp', 'Redesign of frontend', '2025-08-05', '2025-09-10', 'completed'),
('Mobile App Launch', 'Development of the new mobile application', '2025-08-10', '2025-10-01', 'active'),
('Marketing Campaign', 'Plan and execute fall marketing campaign', '2025-08-15', '2025-09-30', 'planned');

INSERT INTO tasks (title, assigned_to, status, due_date, project_id)
VALUES
('Setup API', 'Alice', 'pending', '2025-08-10', 1),
('Integrate MCP', 'Bob', 'overdue', '2025-08-05', 1),
('Create Test Cases', 'Dana', 'in_progress', '2025-08-15', 1),
('Deploy API', 'Eve', 'pending', '2025-08-20', 1),
('UI Mockups', 'Charlie', 'completed', '2025-08-15', 2),
('Frontend Integration', 'Frank', 'pending', '2025-08-25', 2),
('Develop Mobile UI', 'Grace', 'in_progress', '2025-08-20', 3),
('Setup Firebase', 'Heidi', 'pending', '2025-08-22', 3),
('Draft Marketing Plan', 'Ivan', 'pending', '2025-08-18', 4),
('Design Ad Creatives', 'Judy', 'planned', '2025-08-25', 4);