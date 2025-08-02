from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def init_db(app):
    """Configure and initialize the database with SQLAlchemy."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='new')
    tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan")

    def as_dict(self):
        """Convert Project model to a JSON-serializable dictionary."""
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            data[column.name] = value
        return data


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20))
    due_date = db.Column(db.Date, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    def as_dict(self):
        """Convert Task model to a JSON-serializable dictionary."""
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            data[column.name] = value
        return data
