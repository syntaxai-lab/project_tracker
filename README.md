# project_tracker
AI-powered Project Tracker enabling agents to log tasks, fetch updates, and analyze progress via LLM queries. Includes a backend API for project data and an MCP tool connected to the LLM for status retrieval, filtering, and task management.

## Features
- **LLM-powered query interpretation**: The agent uses an LLM to understand natural language queries and extract filters dynamically.
- **Dynamic entity detection**: The agent distinguishes between project and task queries without hardcoded keyword checks.
- **Dockerized setup**: Includes containers for the API, database, and MCP-compatible agent.
- **Automatic database seeding**: The seeder initializes tables and loads sample data for testing.
- **Interactive CLI**: Run the agent and ask multiple questions in a single session.

## Setup Instructions (Using Docker)

This project runs entirely with Docker. You only need **Docker Desktop** installed.

### Steps to Run
1. **Start containers** for the API, database, and agent:
   ```bash
   docker compose up --build
   ```

2. **Database Initialization and Seeding**
   - The database tables are initialized and sample data is loaded automatically by the seeder service.
   - To run the seeder manually:
     ```bash
     docker compose run seeder
     ```

3. **Run the agent** interactively to ask questions:
   ```bash
   docker compose run agent python agent.py
   ```
   - The CLI will prompt:
     ```
     Ask your questions (press 0 to exit):
     ```
   - Enter your question, for example:
     ```
     how many projects are overdue
     ```
   - Example CLI output:
     ```
     [+] Creating 2/0
      ✔ Container project_tracker_db   Running
      ✔ Container project_tracker_api  Running
     Ask your questions (press 0 to exit):
     > how many projects are overdue
     INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
     INFO:root:[AGENT] Calling API with filters: {'entity': 'projects', 'status': 'overdue'}
     INFO:root:[MCP] Fetching projects with filters: {'status': 'overdue'}
     INFO:root:[AGENT] API responded: {'filters': {'entity': 'projects', 'status': 'overdue'}, 'results': [{'id': 4, 'name': 'Marketing Campaign', 'status': 'overdue'}]}
     {'filters': {'entity': 'projects', 'status': 'overdue'}, 'results': [{'id': 4, 'name': 'Marketing Campaign', 'status': 'overdue'}]}
     ```

5. **Architecture Diagram**
![Architecture Diagram](architecture.drawio.png)

---

## Testing with Postman

You can also test the backend API using the provided **Postman Collection**:

1. Import the file `project_tracker_postman.json` into Postman.
2. Start the containers with:
   ```bash
   docker compose up
   ```
3. Initialize the database by calling the `initdb` request in the collection.
4. Use the `Create Project` and `Create Task` requests to add data.
5. Test `Get Projects` and `Get Tasks` endpoints to verify filtering and retrieval.

---

## Interacting with the Database Directly

To manually inspect or test the PostgreSQL database:

1. Enter the running database container:
   ```bash
   docker exec -it project_tracker_db psql -U user -d project_db
   ```
2. Run SQL commands, for example:
   ```sql
   \dt          -- list tables
   SELECT * FROM projects;
   SELECT * FROM tasks;
   ```
3. Exit the database shell:
   ```
   \q
   ```

---

## Tests Folder

The `tests/` folder is included for adding unit or integration tests. Currently, it has no tests implemented.  
You can add `pytest`-based tests here to verify API endpoints and MCP agent behavior, for example:

```bash
pytest tests/
```