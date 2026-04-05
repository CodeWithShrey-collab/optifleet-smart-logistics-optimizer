from app.routes.auth_routes import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.dispatch_routes import dispatch_bp
from app.routes.network_routes import network_bp
from app.routes.optimizer_routes import optimizer_bp
from app.routes.order_routes import order_bp
from app.routes.vehicle_routes import vehicle_bp
from app.routes.warehouse_routes import warehouse_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(dispatch_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(optimizer_bp)
