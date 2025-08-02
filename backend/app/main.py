from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime
from database import init_db, db, Project, Task


""""1. Create a new project with the fields: name, description,
start_date, end_date, and status
2. Add a task to a project with: title, assigned_to, status, due_date,
project_id
3. Retrieve a project and its associated tasks
4. Query/filter projects by fields"""

# This flask app is going to be an api
app = Flask(__name__)
api = Api(app)

# Initialize DB
init_db(app)

EXPECTED_PROJECT_FIELDS = ["name", "description", "start_date", "end_date", "status"]
EXPECTED_TASK_FIELDS = ["title", "assigned_to", "status", "due_date", "project_id"]


class ProjectResource(Resource):
    """Handles HTTP requests for projects including creation, retrieval, and filtering."""
    def get(self, project_id=None):
        try:
            if project_id:
                proj = Project.query.get(project_id)
                if proj:
                    tasks_list = [t.as_dict() for t in proj.tasks]
                    proj_dict = proj.as_dict()
                    proj_dict["tasks"] = tasks_list
                    return proj_dict
                return {"error": "Not found"}, 404
            query = Project.query
            for key, value in request.args.items():
                if not hasattr(Project, key):
                    return {"error": f"Invalid filter field: {key}"}, 400
                query = query.filter(getattr(Project, key).ilike(f"%{value}%"))
            results = [p.as_dict() for p in query.all()]
            return results
        except Exception as e:
            return {"error": f"Internal server error: {str(e)}"}, 500

    def post(self):
        try:
            raw_data = request.get_json() or {}
            project_data = normalize_input(raw_data, EXPECTED_PROJECT_FIELDS)
            error_msg = validate_project_data(project_data)
            if error_msg:
                return {"error": error_msg}, 400

            proj = Project(**project_data)
            db.session.add(proj)
            db.session.commit()
            return proj.as_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Internal server error: {str(e)}"}, 500


class TaskResource(Resource):
    """Handles HTTP requests for tasks including creation, retrieval, and filtering."""
    def post(self):
        try:
            raw_data = request.get_json() or {}
            task_data = normalize_input(raw_data, EXPECTED_TASK_FIELDS)
            error_msg = validate_task_data(task_data)
            if error_msg:
                return {"error": error_msg}, 400

            task = Task(**task_data)
            db.session.add(task)
            db.session.commit()
            return task.as_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Internal server error: {str(e)}"}, 500

    def get(self, task_id=None, project_id=None):
        try:
            if task_id:
                task = Task.query.get(task_id)
                if task:
                    return task.as_dict()
                return {"error": "Task not found"}, 404
            if project_id:
                proj = Project.query.get(project_id)
                if not proj:
                    return {"error": "Project not found"}, 404
                return [t.as_dict() for t in proj.tasks]
            query = Task.query
            for key, value in request.args.items():
                if not hasattr(Task, key):
                    return {"error": f"Invalid filter field: {key}"}, 400
                query = query.filter(getattr(Task, key).ilike(f"%{value}%"))
            return [t.as_dict() for t in query.all()]
        except Exception as e:
            return {"error": f"Internal server error: {str(e)}"}, 500


# --- Test Resource classes ---
class InitDBResource(Resource):
    """Handles manual initialization of the database tables."""
    def get(self):
        try:
            with app.app_context():
                db.create_all()
            return {"message": "Database initialized!"}, 200
        except Exception as e:
            return {"error": f"Failed to initialize database: {str(e)}"}, 500


class TestResource(Resource):
    """Simple test endpoint to verify API is running."""
    def get(self):
        return {"message": "test route"}, 200


def normalize_input(data, expected_fields):
    """Convert incoming JSON keys to lowercase and retain only expected fields."""
    normalized = {}
    for key, value in data.items():
        key_lower = key.lower()
        if key_lower in expected_fields:
            normalized[key_lower] = value
    return normalized


def validate_project_data(data):
    """Validate project data, ensuring required fields exist and dates are formatted correctly."""
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
    """Validate task data, ensuring required fields exist, dates are valid, and project_id is valid."""
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
    if not Project.query.get(data["project_id"]):
        return "Invalid project_id. Project does not exist."
    return None


api.add_resource(InitDBResource, "/initdb")
api.add_resource(TestResource, "/test")
api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
api.add_resource(TaskResource, "/tasks", "/tasks/<int:task_id>", "/projects/<int:project_id>/tasks")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)  # port 5000 in use
