from flask import Flask, jsonify, render_template, request

from app.config import Config
from app.extensions import init_extensions
from app.models import db
from app.routes import register_routes


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    init_extensions(app)
    register_routes(app)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        if request.path.startswith("/api/"):
            return jsonify({"status": "error", "message": "Resource not found."}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        return jsonify({"status": "error", "message": "An unexpected server error occurred."}), 500
