"""
Form validation, kept separate from routes on purpose.

Why: validation rules change independently of routing logic, and testing
"is this phone number valid" shouldn't require spinning up Flask. Each
validate_* function returns (errors: list[str], cleaned_data: dict) so a
route just checks `if errors: ... else: use cleaned_data`.
"""

import re

PHONE_RE = re.compile(r"^\+?[0-9\s\-]{7,15}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _to_float(value, field_name, errors, min_value=0):
    try:
        num = float(value)
    except (TypeError, ValueError):
        errors.append(f"{field_name} must be a number.")
        return None
    if num < min_value:
        errors.append(f"{field_name} cannot be negative.")
        return None
    return num


def _to_int(value, field_name, errors):
    try:
        return int(value)
    except (TypeError, ValueError):
        errors.append(f"{field_name} must be a whole number.")
        return None


def validate_customer(form):
    errors = []
    name = (form.get("customer_name") or "").strip()
    phone = (form.get("phone") or "").strip()
    email = (form.get("email") or "").strip()

    if not name:
        errors.append("Customer name is required.")
    elif len(name) > 100:
        errors.append("Customer name is too long (max 100 characters).")

    if not phone:
        errors.append("Phone number is required.")
    elif not PHONE_RE.match(phone):
        errors.append("Phone number doesn't look valid (use digits, spaces, +, -).")

    if email and not EMAIL_RE.match(email):
        errors.append("Email address doesn't look valid.")

    return errors, {"customer_name": name, "phone": phone, "email": email}


def validate_trip(form):
    errors = []

    customer_id = _to_int(form.get("customer_id"), "Customer", errors)
    pickup = (form.get("pickup") or "").strip()
    destination = (form.get("destination") or "").strip()
    vehicle = (form.get("vehicle") or "").strip()
    driver = (form.get("driver") or "").strip()
    payment_method = (form.get("payment_method") or "").strip()
    trip_date = (form.get("trip_date") or "").strip()

    fare = _to_float(form.get("fare"), "Fare", errors, min_value=0.01)
    fuel_cost_raw = form.get("fuel_cost") or "0"
    fuel_cost = _to_float(fuel_cost_raw, "Fuel cost", errors, min_value=0)

    if not pickup:
        errors.append("Pickup location is required.")
    if not destination:
        errors.append("Destination is required.")
    if pickup and destination and pickup.lower() == destination.lower():
        errors.append("Pickup and destination can't be the same place.")
    if not vehicle:
        errors.append("Vehicle is required.")
    if not trip_date:
        errors.append("Trip date is required.")

    return errors, {
        "customer_id": customer_id,
        "pickup": pickup,
        "destination": destination,
        "vehicle": vehicle,
        "driver": driver,
        "fare": fare,
        "fuel_cost": fuel_cost,
        "payment_method": payment_method,
        "trip_date": trip_date,
    }


def validate_status(status, valid_statuses):
    errors = []
    if status not in valid_statuses:
        errors.append("That's not a recognized trip status.")
    return errors
