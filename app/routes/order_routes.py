from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from app.extensions import db
from app.models import Order
from app.utils.helpers import get_request_data
from app.utils.validators import parse_order_payload


order_bp = Blueprint("orders", __name__)


@order_bp.get("/orders")
@login_required
def orders_page():
    return render_template("orders/index.html")


@order_bp.get("/api/orders")
@login_required
def list_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify({"status": "success", "data": [order.to_dict() for order in orders]})


@order_bp.post("/api/orders")
@login_required
def create_order():
    payload = get_request_data(request)
    cleaned_data, errors = parse_order_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    order = Order(**cleaned_data)
    db.session.add(order)
    db.session.commit()
    return jsonify({"status": "success", "message": "Order created.", "data": order.to_dict()}), 201


@order_bp.get("/api/orders/<int:order_id>")
@login_required
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({"status": "success", "data": order.to_dict()})


@order_bp.put("/api/orders/<int:order_id>")
@login_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    payload = get_request_data(request)
    cleaned_data, errors = parse_order_payload(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    order.update_from_dict(cleaned_data)
    db.session.commit()
    return jsonify({"status": "success", "message": "Order updated.", "data": order.to_dict()})


@order_bp.delete("/api/orders/<int:order_id>")
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"status": "success", "message": "Order deleted."})
