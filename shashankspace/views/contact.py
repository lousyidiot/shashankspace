from flask import Blueprint, render_template, request
from flask.views import MethodView

contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

class ContactPage(MethodView):
    def get(self):
        return render_template("contact.html", title="Contact")

    def post(self):
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        return f"Thanks {name}, your message has been received!"

contact_bp.add_url_rule("/", view_func=ContactPage.as_view("contact"), methods=["GET", "POST"])
