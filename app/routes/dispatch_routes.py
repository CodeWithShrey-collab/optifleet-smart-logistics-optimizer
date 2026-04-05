from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app.models import Order
from app.services.activity_selection_service import select_activities
from app.services.hamiltonian_service import hamiltonian_cycle
from app.services.max_subarray_service import max_subarray


dispatch_bp = Blueprint("dispatch", __name__)


@dispatch_bp.get("/dispatch")
@login_required
def dispatch_page():
    return render_template("dispatch/index.html")


@dispatch_bp.post("/dispatch/run")
@login_required
def run_dispatch():
    orders = Order.query.filter_by(status="pending").order_by(Order.delivery_end.asc(), Order.id.asc()).all()
    tasks = [_serialize_order_for_dispatch(order) for order in orders]

    selected = select_activities(tasks)
    selected_small = selected[:6]
    graph = _build_dispatch_graph(len(selected_small))
    route_indices = hamiltonian_cycle(graph)
    route_details = _map_route_details(route_indices, selected_small)
    route_summary = _build_route_summary(route_details)

    profits = [task["profit"] for task in selected]
    profit_analysis = max_subarray(profits) if profits else {}
    profit_window = _profit_window(selected, profit_analysis)
    profit_summary = _build_profit_summary(profit_analysis, profit_window)

    return jsonify(
        {
            "status": "success",
            "data": {
                "pending_order_count": len(tasks),
                "selected": [_format_task(task) for task in selected],
                "route": route_indices,
                "route_details": route_details,
                "route_summary": route_summary,
                "profit_analysis": profit_analysis,
                "profit_window": profit_window,
                "profit_summary": profit_summary,
            },
        }
    )


def _serialize_order_for_dispatch(order):
    start_minutes = int(order.delivery_start.timestamp() // 60)
    end_minutes = int(order.delivery_end.timestamp() // 60)
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "package_name": order.package_name,
        "start": start_minutes,
        "end": end_minutes,
        "profit": order.profit,
        "destination": order.destination,
        "delivery_start": order.delivery_start.isoformat(),
        "delivery_end": order.delivery_end.isoformat(),
    }


def _format_task(task):
    return {
        "id": task["id"],
        "customer_name": task["customer_name"],
        "package_name": task["package_name"],
        "profit": task["profit"],
        "destination": task["destination"],
        "delivery_start": task["delivery_start"],
        "delivery_end": task["delivery_end"],
    }


def _build_dispatch_graph(size):
    return [[1 if row != column else 0 for column in range(size)] for row in range(size)]


def _map_route_details(route_indices, selected_small):
    if not selected_small:
        return []

    if len(selected_small) == 1:
        task = selected_small[0]
        return [
            {
                "route_index": 0,
                "order_id": task["id"],
                "destination": task["destination"],
                "customer_name": task["customer_name"],
                "package_name": task["package_name"],
                "is_return_to_start": False,
            }
        ]

    if not route_indices:
        return []

    details = []
    for position, index in enumerate(route_indices):
        task = selected_small[index]
        details.append(
            {
                "route_index": index,
                "order_id": task["id"],
                "destination": task["destination"],
                "customer_name": task["customer_name"],
                "package_name": task["package_name"],
                "is_return_to_start": position == len(route_indices) - 1,
            }
        )
    return details


def _profit_window(selected, profit_analysis):
    if not selected or not profit_analysis:
        return []

    start_index = profit_analysis["start_index"]
    end_index = profit_analysis["end_index"] + 1
    return [_format_task(task) for task in selected[start_index:end_index]]


def _build_route_summary(route_details):
    if not route_details:
        return "No route could be generated from the selected deliveries."

    if len(route_details) == 1:
        return f"Single-stop dispatch to {route_details[0]['destination']}."

    visible_stops = [stop["destination"] for stop in route_details[:-1]] if route_details[-1]["is_return_to_start"] else [
        stop["destination"] for stop in route_details
    ]
    if route_details[-1]["is_return_to_start"]:
        return f"Dispatch sequence: {' -> '.join(visible_stops)} -> return to origin."
    return f"Dispatch sequence: {' -> '.join(visible_stops)}."


def _build_profit_summary(profit_analysis, profit_window):
    if not profit_analysis or not profit_window:
        return "No profit analysis available."

    if len(profit_window) == 1:
        item = profit_window[0]
        return f"Best profit opportunity is Order #{item['id']} worth {item['profit']:.2f}."

    return (
        f"Best profit streak totals {profit_analysis['max_sum']:.2f} "
        f"across {len(profit_window)} consecutive selected deliveries."
    )
