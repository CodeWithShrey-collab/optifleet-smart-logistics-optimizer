from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy import and_

from app.extensions import db
from app.models import Warehouse
from app.utils.helpers import get_request_data
from app.utils.validators import parse_warehouse_payload


warehouse_bp = Blueprint("warehouses", __name__)


@warehouse_bp.get("/warehouses")
@login_required
def warehouses_page():
    return render_template("warehouses/index.html")


@warehouse_bp.get("/api/warehouses")
@login_required
def list_warehouses():
    warehouses = Warehouse.query.order_by(Warehouse.name.asc()).all()
    return jsonify({"status": "success", "data": [warehouse.to_dict() for warehouse in warehouses]})


@warehouse_bp.post("/api/warehouses")
@login_required
def create_warehouse():
    payload = get_request_data(request)
    cleaned_data, errors = parse_warehouse_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    duplicate = Warehouse.query.filter(
        and_(Warehouse.name == cleaned_data["name"], Warehouse.city == cleaned_data["city"])
    ).first()
    if duplicate:
        return jsonify({"status": "error", "message": "A warehouse with this name already exists in the selected city."}), 409

    warehouse = Warehouse(**cleaned_data)
    db.session.add(warehouse)
    db.session.commit()
    return jsonify({"status": "success", "message": "Warehouse created.", "data": warehouse.to_dict()}), 201


@warehouse_bp.get("/api/warehouses/<int:warehouse_id>")
@login_required
def get_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    return jsonify({"status": "success", "data": warehouse.to_dict()})


@warehouse_bp.put("/api/warehouses/<int:warehouse_id>")
@login_required
def update_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    payload = get_request_data(request)
    cleaned_data, errors = parse_warehouse_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    duplicate = Warehouse.query.filter(
        and_(
            Warehouse.name == cleaned_data["name"],
            Warehouse.city == cleaned_data["city"],
            Warehouse.id != warehouse_id,
        )
    ).first()
    if duplicate:
        return jsonify({"status": "error", "message": "A warehouse with this name already exists in the selected city."}), 409

    warehouse.update_from_dict(cleaned_data)
    db.session.commit()
    return jsonify({"status": "success", "message": "Warehouse updated.", "data": warehouse.to_dict()})


@warehouse_bp.delete("/api/warehouses/<int:warehouse_id>")
@login_required
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    db.session.delete(warehouse)
    db.session.commit()
    return jsonify({"status": "success", "message": "Warehouse deleted."})
