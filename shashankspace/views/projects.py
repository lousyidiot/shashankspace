from flask import Blueprint, render_template
from flask.views import MethodView

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")

class ProjectsPage(MethodView):
    def get(self):
        projects = [
            {"name": "Personal Website", "desc": "Built with Flask"},
            {"name": "AI Detector", "desc": "Detect AI-generated text"}
        ]
        return render_template("projects.html", title="Projects", projects=projects)

projects_bp.add_url_rule("/", view_func=ProjectsPage.as_view("projects"))
