from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models import User
from app.utils.helpers import get_request_data
from app.utils.validators import validate_login_payload, validate_registration_payload


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    return render_template("auth/login.html")


@auth_bp.post("/login")
def login_action():
    payload = get_request_data(request)
    errors = validate_login_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    user = User.query.filter_by(email=payload["email"].strip().lower()).first()
    if user is None or not user.check_password(payload["password"]):
        return jsonify({"status": "error", "message": "Invalid email or password."}), 401

    login_user(user)
    return jsonify(
        {"status": "success", "message": "Login successful.", "redirect_url": url_for("dashboard.dashboard_page")}
    )


@auth_bp.get("/register")
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    return render_template("auth/register.html")


@auth_bp.post("/register")
def register_action():
    payload = get_request_data(request)
    errors = validate_registration_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    existing_user = User.query.filter_by(email=payload["email"].strip().lower()).first()
    if existing_user:
        return jsonify({"status": "error", "message": "An account with this email already exists."}), 409

    user = User(
        name=payload["name"].strip(),
        email=payload["email"].strip().lower(),
        role=payload.get("role", "operator").strip() or "operator",
    )
    user.set_password(payload["password"])
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify(
        {"status": "success", "message": "Account created successfully.", "redirect_url": url_for("dashboard.dashboard_page")}
    ), 201


@auth_bp.post("/logout")
@login_required
def logout_action():
    logout_user()
    return jsonify({"status": "success", "message": "Logged out.", "redirect_url": url_for("auth.login_page")})
