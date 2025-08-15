from flask import Blueprint, render_template
from flask.views import MethodView

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")

class ResumePage(MethodView):
    def get(self):
        return render_template("resume.html", title="Resume")

resume_bp.add_url_rule("/", view_func=ResumePage.as_view("resume"))
