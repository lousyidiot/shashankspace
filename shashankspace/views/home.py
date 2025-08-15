from flask import Blueprint, render_template
from flask.views import MethodView

home_bp = Blueprint("home", __name__)

class HomePage(MethodView):
    def get(self):
        return render_template("home.html", title="Shashank Space - Home")

home_bp.add_url_rule("/", view_func=HomePage.as_view("home"))
