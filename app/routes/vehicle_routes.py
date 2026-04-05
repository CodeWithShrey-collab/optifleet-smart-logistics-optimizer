from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import and_

from app.extensions import db
from app.models import Vehicle
from app.utils.helpers import get_request_data
from app.utils.validators import parse_vehicle_payload


vehicle_bp = Blueprint("vehicles", __name__)


@vehicle_bp.get("/vehicles")
@login_required
def vehicles_page():
    return render_template("vehicles/index.html")


@vehicle_bp.get("/api/vehicles")
@login_required
def list_vehicles():
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return jsonify({"status": "success", "data": [vehicle.to_dict() for vehicle in vehicles]})


@vehicle_bp.post("/api/vehicles")
@login_required
def create_vehicle():
    payload = get_request_data(request)
    cleaned_data, errors = parse_vehicle_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    if Vehicle.query.filter_by(truck_name=cleaned_data["truck_name"]).first():
        return jsonify({"status": "error", "message": "Truck name already exists."}), 409

    vehicle = Vehicle(**cleaned_data)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"status": "success", "message": "Vehicle created.", "data": vehicle.to_dict()}), 201


@vehicle_bp.get("/api/vehicles/<int:vehicle_id>")
@login_required
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({"status": "success", "data": vehicle.to_dict()})


@vehicle_bp.put("/api/vehicles/<int:vehicle_id>")
@login_required
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    payload = get_request_data(request)
    cleaned_data, errors = parse_vehicle_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    duplicate = Vehicle.query.filter(and_(Vehicle.truck_name == cleaned_data["truck_name"], Vehicle.id != vehicle_id)).first()
    if duplicate:
        return jsonify({"status": "error", "message": "Truck name already exists."}), 409

    vehicle.update_from_dict(cleaned_data)
    db.session.commit()
    return jsonify({"status": "success", "message": "Vehicle updated.", "data": vehicle.to_dict()})


@vehicle_bp.delete("/api/vehicles/<int:vehicle_id>")
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"status": "success", "message": "Vehicle deleted."})
