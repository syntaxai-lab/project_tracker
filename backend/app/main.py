from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime


""""1. Create a new project with the fields: name, description,
start_date, end_date, and status
2. Add a task to a project with: title, assigned_to, status, due_date,
project_id
3. Retrieve a project and its associated tasks
4. Query/filter projects by fields"""

# This flask app is going to be an api
app = Flask(__name__)
api = Api(app)

projects = []
tasks = []
EXPECTED_PROJECT_FIELDS = ["name", "description", "start_date", "end_date", "status"]
EXPECTED_TASK_FIELDS = ["title", "assigned_to", "status", "due_date", "project_id"]


class Project():
    def __init__(self, name, description, start_date, end_date, status='new'):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status


class ProjectResource(Resource):
    def get(self, project_id=None):
        if project_id:
            proj = next((p.casefold() for p in projects if p['id'] == project_id), None)
            if proj:
                proj_tasks = [t for t in tasks if t.get("project_id")
                              == project_id]
                proj["tasks"] = proj_tasks
                return proj
            return {"error": "Not found"}, 404
        filters = request.args
        results = projects
        for key, value in filters.items():
            results = [p for p in results if str(p.get(key)).lower() ==
                       value.lower()]
        return results

    def post(self):
        raw_data = request.get_json() or {}
        project_data = normalize_input(raw_data, EXPECTED_PROJECT_FIELDS)
        error_msg = validate_project_data(project_data)
        if error_msg:
            return {"error": error_msg}, 400

        proj = Project(**project_data)
        new_project = proj.__dict__
        new_project['id'] = len(projects) + 1
        projects.append(new_project)
        return new_project, 201


class TaskResource(Resource):
    def post(self):
        raw_data = request.get_json() or {}
        task_data = normalize_input(raw_data, EXPECTED_TASK_FIELDS)
        error_msg = validate_task_data(task_data)
        if error_msg:
            return {"error": error_msg}, 400

        new_task = {**task_data, "id": len(tasks) + 1}
        tasks.append(new_task)
        return new_task, 201

    def get(self, task_id=None, project_id=None):
        if task_id:
            task = next((t for t in tasks if t["id"] == task_id), None)
            if task:
                return task
            return {"error": "Task not found"}, 404
        if project_id:
            project_exists = any(p["id"] == project_id for p in projects)
            if not project_exists:
                return {"error": "Project not found"}, 404

            project_tasks = [t for t in tasks if t.get("project_id") == project_id]
            return project_tasks
        # Otherwise return all (with optional filters)
        filters = request.args
        results = tasks
        for key, value in filters.items():
            results = [t for t in results if str(t.get(key)).lower()
                       == value.lower()]
        return results


def normalize_input(data, expected_fields):
    """Normalize keys to lowercase and map to expected fields."""
    normalized = {}
    for key, value in data.items():
        key_lower = key.lower()
        if key_lower in expected_fields:
            normalized[key_lower] = value
    return normalized


def validate_project_data(data):
    """Validate required fields and date formats."""
    required_fields = ["name", "description", "start_date", "end_date"]
    for field in required_fields:
        if field not in data:
            return f"Missing or Incorrect required field: {field}"
    # Validate date format
    for date_field in ["start_date", "end_date"]:
        try:
            datetime.strptime(data[date_field], "%Y-%m-%d")
        except ValueError:
            return f"Invalid date format for {date_field}. \
        Expected YYYY-MM-DD."
    return None


def validate_task_data(data):
    """Validate required fields and date formats."""
    required_fields = ["title", "assigned_to", "due_date", "project_id"]
    for field in required_fields:
        if field not in data:
            return f"Missing or Incorrect required field: {field}"
    # Validate date format
    try:
        datetime.strptime(data["due_date"], "%Y-%m-%d")
    except ValueError:
        return "Invalid date format for due_date. Expected YYYY-MM-DD."
    # Validate project_id exists
    if not any(p["id"] == data["project_id"] for p in projects):
        return "Invalid project_id. Project does not exist."
    return None


api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
api.add_resource(TaskResource, "/tasks", "/tasks/<int:task_id>", "/projects/<int:project_id>/tasks")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)  # port 5000 in use
