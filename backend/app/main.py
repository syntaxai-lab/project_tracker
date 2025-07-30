from flask import Flask, request
from flask_restful import Api, Resource


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
            proj = next((p for p in projects if p['id'] == project_id), None)
            if proj:
                proj_tasks = [t for t in tasks if t.get("project_id")
                              == project_id]
                proj["tasks"] = proj_tasks
                return proj
            return {"error": "Not found"}, 404
        filters = request.args
        results = projects
        for key, value in filters.items():
            results = [p for p in results if str(p.get(key)) == value]
        return results

    def post(self):
        data = request.get_json()
        proj = Project(**data)  # instantiate
        new_project = proj.__dict__  # turn into dict
        new_project['id'] = len(projects) + 1
        projects.append(new_project)
        return new_project, 201


class TaskResource(Resource):
    def post(self):
        data = request.get_json()
        new_task = {**data, "id": len(tasks) + 1}
        tasks.append(new_task)
        return new_task, 201


api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
api.add_resource(TaskResource, "/tasks")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050) # port 5000 in use


    """Bash output:
parasjamil@Parass-MacBook-Pro project_tracker % curl -X POST http://127.0.0.1:5050/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"AI Tracker","description":"Demo","start_date":"2025-07-28","end_date":"2025-08-28"}'
{"name": "AI Tracker", "description": "Demo", "start_date": "2025-07-28", "end_date": "2025-08-28", "status": "new", "id": 1}
parasjamil@Parass-MacBook-Pro project_tracker % curl http://127.0.0.1:5050/projects
[{"name": "AI Tracker", "description": "Demo", "start_date": "2025-07-28", "end_date": "2025-08-28", "status": "new", "id": 1}]
parasjamil@Parass-MacBook-Pro project_tracker % curl http://127.0.0.1:5050/projects/1
{"name": "AI Tracker", "description": "Demo", "start_date": "2025-07-28", "end_date": "2025-08-28", "status": "new", "id": 1}
    """
