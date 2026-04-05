from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app.models import Warehouse
from app.services.mst_service import build_warehouse_edges, compute_mst


network_bp = Blueprint("network", __name__)


@network_bp.get("/network")
@login_required
def network_page():
    warehouses = Warehouse.query.order_by(Warehouse.name.asc()).all()
    return render_template("network/index.html", warehouses=warehouses)


@network_bp.post("/network/run")
@login_required
def run_network():
    warehouses = Warehouse.query.order_by(Warehouse.name.asc()).all()
    nodes = [warehouse.id for warehouse in warehouses]

    if len(nodes) < 2:
        return jsonify(
            {
                "status": "success",
                "data": {
                    "warehouses": [_serialize_warehouse(warehouse) for warehouse in warehouses],
                    "mst": [],
                    "total_cost": 0,
                    "summary": "Add at least two warehouses to compute an optimized network.",
                    "is_connected": False,
                },
            }
        )

    edges = build_warehouse_edges(warehouses)
    mst_edges, total_cost = compute_mst(nodes, edges)
    warehouse_lookup = {warehouse.id: warehouse for warehouse in warehouses}
    mst_with_labels = [_decorate_edge(edge, warehouse_lookup) for edge in mst_edges]
    is_connected = len(mst_edges) == len(nodes) - 1

    return jsonify(
        {
            "status": "success",
            "data": {
                "warehouses": [_serialize_warehouse(warehouse) for warehouse in warehouses],
                "mst": mst_with_labels,
                "total_cost": total_cost,
                "summary": _build_network_summary(len(nodes), len(mst_edges), total_cost, is_connected),
                "is_connected": is_connected,
            },
        }
    )


def _serialize_warehouse(warehouse):
    return {
        "id": warehouse.id,
        "name": warehouse.name,
        "city": warehouse.city,
        "latitude": warehouse.latitude,
        "longitude": warehouse.longitude,
    }


def _decorate_edge(edge, warehouse_lookup):
    source = warehouse_lookup[edge["u"]]
    target = warehouse_lookup[edge["v"]]
    return {
        "u": edge["u"],
        "v": edge["v"],
        "weight": edge["weight"],
        "from_name": source.name,
        "from_city": source.city,
        "to_name": target.name,
        "to_city": target.city,
    }


def _build_network_summary(node_count, edge_count, total_cost, is_connected):
    if not is_connected:
        return "The current warehouse graph could not form a fully connected minimum spanning tree."
    return (
        f"Optimized {node_count} warehouses with {edge_count} low-cost links. "
        f"Estimated total network distance: {total_cost:.2f} km."
    )
