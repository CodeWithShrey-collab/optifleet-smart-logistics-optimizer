from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from sqlalchemy import func

from app.models import Order, Vehicle


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
@login_required
def root_redirect():
    return render_template("dashboard/dashboard.html")


@dashboard_bp.get("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard/dashboard.html")


@dashboard_bp.get("/api/dashboard/summary")
@login_required
def dashboard_summary():
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status="pending").count()
    available_vehicles = Vehicle.query.filter_by(status="available").count()
    total_profit = float(Order.query.session.query(func.sum(Order.profit)).scalar() or 0)

    status_rows = (
        Order.query.with_entities(Order.status, func.count(Order.id))
        .group_by(Order.status)
        .order_by(Order.status.asc())
        .all()
    )
    return jsonify(
        {
            "status": "success",
            "data": {
                "kpis": {
                    "total_orders": total_orders,
                    "pending_orders": pending_orders,
                    "available_vehicles": available_vehicles,
                    "total_profit": total_profit,
                },
                "status_breakdown": [{"status": status, "count": count} for status, count in status_rows],
            },
        }
    )
