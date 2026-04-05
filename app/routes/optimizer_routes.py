from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from app.models import Order, Vehicle
from app.services.knapsack_service import fractional_knapsack
from app.utils.helpers import get_request_data
from app.utils.validators import parse_optimizer_payload


optimizer_bp = Blueprint("optimizer", __name__)


@optimizer_bp.get("/optimizer")
@login_required
def optimizer_page():
    return render_template("optimizer/index.html")


@optimizer_bp.get("/api/optimizer/context")
@login_required
def optimizer_context():
    vehicles = Vehicle.query.order_by(Vehicle.truck_name.asc()).all()
    orders = Order.query.filter_by(status="pending").order_by(Order.created_at.desc()).all()
    return jsonify(
        {
            "status": "success",
            "data": {
                "vehicles": [vehicle.to_dict() for vehicle in vehicles],
                "orders": [order.to_dict() for order in orders],
            },
        }
    )


@optimizer_bp.post("/api/optimizer/knapsack")
@login_required
def knapsack_optimizer():
    payload = get_request_data(request)
    cleaned_data, errors = parse_optimizer_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    vehicle = Vehicle.query.get(cleaned_data["vehicle_id"])
    if vehicle is None:
        return jsonify({"status": "error", "message": "Vehicle not found."}), 404

    orders = Order.query.filter(Order.id.in_(cleaned_data["order_ids"]), Order.status == "pending").all()
    if not orders:
        return jsonify({"status": "error", "message": "No pending orders matched the selection."}), 404

    remaining_capacity = max(vehicle.capacity - vehicle.current_load, 0)
    selected_items, total_value = fractional_knapsack(
        remaining_capacity,
        [
            {
                "id": order.id,
                "package_name": order.package_name,
                "customer_name": order.customer_name,
                "weight": order.weight,
                "value": order.profit,
                "priority": order.priority,
                "destination": order.destination,
            }
            for order in orders
        ],
    )
    return jsonify(
        {
            "status": "success",
            "data": {
                "vehicle": vehicle.to_dict(),
                "remaining_capacity": remaining_capacity,
                "selected_items": selected_items,
                "total_value": total_value,
            },
        }
    )
