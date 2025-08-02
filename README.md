# project_tracker
AI-powered Project Tracker enabling agents to log tasks, fetch updates, and analyze progress via LLM queries. Includes a backend API for project data and an MCP tool connected to the LLM for status retrieval, filtering, and task management.

## Setup Instructions

### Local Development (Optional)
1. Install PostgreSQL on Mac using Homebrew:
   ```bash
   brew install postgresql@14
   brew services start postgresql@14
   ```
2. Create the database:
   ```bash
   createdb project_db
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask API:
   ```bash
   python backend/app/main.py
   ```

### Using Docker Compose
This project includes a Dockerized setup with separate containers for the API and PostgreSQL.

1. Build and start containers:
   ```bash
   docker-compose up --build
   ```
2. The API will be available at:
   ```
   http://localhost:5050
   ```
3. PostgreSQL runs inside its own container and is automatically configured.

---

### Environment Variables
Ensure the API container has the following environment variable set:
```
DATABASE_URL=postgresql://user:password@db:5432/project_db
```
```

### Example Agent Flow with LLM

**User Prompt:**  
"Show me all overdue tasks assigned to Bob"

**Workflow:**  
Prompt → LLM (extract filters) → MCP Tool → Flask API → JSON → Agent Response

**Example Output:**  
```json
{
  "filters": {
    "assigned_to": "Bob",
    "status": "overdue"
  },
  "results": [
    {
      "id": 1,
      "title": "Fix deployment bug",
      "assigned_to": "Bob",
      "status": "overdue",
      "due_date": "2025-07-30",
      "project_id": 2
    }
  ]
}