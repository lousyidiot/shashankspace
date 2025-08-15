from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("shashankspace.config.Config")

    # Register Blueprints
    from shashankspace.views.home import home_bp
    from shashankspace.views.blog import blog_bp
    from shashankspace.views.projects import projects_bp
    from shashankspace.views.resume import resume_bp
    from shashankspace.views.contact import contact_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(contact_bp)

    return app
