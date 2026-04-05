from datetime import datetime

from email_validator import EmailNotValidError, validate_email


DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


def validate_registration_payload(payload):
    errors = {}
    if not payload.get("name", "").strip():
        errors["name"] = "Name is required."
    errors.update(_validate_email_field(payload.get("email")))
    password = payload.get("password", "")
    if len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."
    return errors


def validate_login_payload(payload):
    errors = {}
    errors.update(_validate_email_field(payload.get("email")))
    if not payload.get("password", ""):
        errors["password"] = "Password is required."
    return errors


def parse_order_payload(payload):
    errors = {}
    customer_name = payload.get("customer_name", "").strip()
    package_name = payload.get("package_name", "").strip()
    source = payload.get("source", "").strip()
    destination = payload.get("destination", "").strip()
    status = payload.get("status", "pending").strip().lower()

    if not customer_name:
        errors["customer_name"] = "Customer name is required."
    if not package_name:
        errors["package_name"] = "Package name is required."
    if not source:
        errors["source"] = "Source is required."
    if not destination:
        errors["destination"] = "Destination is required."
    if status not in {"pending", "scheduled", "in_transit", "delivered"}:
        errors["status"] = "Status is invalid."

    weight = _parse_positive_float(payload.get("weight"), "weight", errors)
    profit = _parse_positive_float(payload.get("profit"), "profit", errors)
    priority = _parse_positive_int(payload.get("priority"), "priority", errors)
    delivery_start = _parse_datetime(payload.get("delivery_start"), "delivery_start", errors)
    delivery_end = _parse_datetime(payload.get("delivery_end"), "delivery_end", errors)

    if delivery_start and delivery_end and delivery_end <= delivery_start:
        errors["delivery_end"] = "Delivery end must be after delivery start."

    if errors:
        return {}, errors

    return (
        {
            "customer_name": customer_name,
            "package_name": package_name,
            "weight": weight,
            "profit": profit,
            "priority": priority,
            "source": source,
            "destination": destination,
            "delivery_start": delivery_start,
            "delivery_end": delivery_end,
            "status": status,
        },
        {},
    )


def parse_vehicle_payload(payload):
    errors = {}
    truck_name = payload.get("truck_name", "").strip()
    location = payload.get("location", "").strip()
    status = payload.get("status", "available").strip().lower()

    if not truck_name:
        errors["truck_name"] = "Truck name is required."
    if not location:
        errors["location"] = "Location is required."
    if status not in {"available", "loading", "en_route", "maintenance"}:
        errors["status"] = "Status is invalid."

    capacity = _parse_positive_float(payload.get("capacity"), "capacity", errors)
    current_load = _parse_non_negative_float(payload.get("current_load"), "current_load", errors)
    if capacity is not None and current_load is not None and current_load > capacity:
        errors["current_load"] = "Current load cannot exceed capacity."

    if errors:
        return {}, errors

    return (
        {
            "truck_name": truck_name,
            "capacity": capacity,
            "current_load": current_load,
            "status": status,
            "location": location,
        },
        {},
    )


def parse_optimizer_payload(payload):
    errors = {}
    try:
        vehicle_id = int(payload.get("vehicle_id", 0))
    except (TypeError, ValueError):
        vehicle_id = 0

    raw_order_ids = payload.get("order_ids", [])
    if isinstance(raw_order_ids, str):
        raw_order_ids = [entry for entry in raw_order_ids.split(",") if entry.strip()]

    order_ids = []
    for raw_id in raw_order_ids:
        try:
            order_ids.append(int(raw_id))
        except (TypeError, ValueError):
            errors["order_ids"] = "Order selection is invalid."
            break

    if vehicle_id <= 0:
        errors["vehicle_id"] = "Vehicle is required."
    if not order_ids:
        errors["order_ids"] = "Select at least one order."

    if errors:
        return {}, errors

    return {"vehicle_id": vehicle_id, "order_ids": order_ids}, {}


def parse_warehouse_payload(payload):
    errors = {}
    name = payload.get("name", "").strip()
    city = payload.get("city", "").strip()

    if not name:
        errors["name"] = "Warehouse name is required."
    if not city:
        errors["city"] = "City is required."

    latitude = _parse_float_in_range(payload.get("latitude"), "latitude", -90, 90, errors)
    longitude = _parse_float_in_range(payload.get("longitude"), "longitude", -180, 180, errors)

    if errors:
        return {}, errors

    return (
        {
            "name": name,
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
        },
        {},
    )


def _validate_email_field(email):
    if not email:
        return {"email": "Email is required."}
    try:
        validate_email(email, check_deliverability=False)
        return {}
    except EmailNotValidError:
        return {"email": "Email format is invalid."}


def _parse_positive_float(value, field_name, errors):
    try:
        parsed = float(value)
        if parsed <= 0:
            raise ValueError
        return parsed
    except (TypeError, ValueError):
        errors[field_name] = f"{field_name.replace('_', ' ').title()} must be greater than 0."
        return None


def _parse_non_negative_float(value, field_name, errors):
    try:
        parsed = float(value)
        if parsed < 0:
            raise ValueError
        return parsed
    except (TypeError, ValueError):
        errors[field_name] = f"{field_name.replace('_', ' ').title()} must be 0 or more."
        return None


def _parse_positive_int(value, field_name, errors):
    try:
        parsed = int(value)
        if parsed <= 0:
            raise ValueError
        return parsed
    except (TypeError, ValueError):
        errors[field_name] = f"{field_name.replace('_', ' ').title()} must be a positive integer."
        return None


def _parse_datetime(value, field_name, errors):
    try:
        return datetime.strptime(value, DATETIME_FORMAT)
    except (TypeError, ValueError):
        errors[field_name] = "Use a valid date and time."
        return None


def _parse_float_in_range(value, field_name, minimum, maximum, errors):
    try:
        parsed = float(value)
        if parsed < minimum or parsed > maximum:
            raise ValueError
        return parsed
    except (TypeError, ValueError):
        errors[field_name] = f"{field_name.replace('_', ' ').title()} must be between {minimum} and {maximum}."
        return None
