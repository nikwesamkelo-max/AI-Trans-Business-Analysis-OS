from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    create_tables,
    add_customer,
    view_customers,
    add_trip,
    view_trips,
    update_trip_status,
)
from analytics import get_dashboard_data

app = Flask(__name__)
app.secret_key = "dev-only-change-this-before-deploying"  # placeholder, fine for local dev

# Maps a trip status to how far along the route line the marker sits (%)
STATUS_PROGRESS = {
    "Booked": 5,
    "Driver Assigned": 30,
    "In Progress": 65,
    "Completed": 100,
    "Cancelled": 0,
}

STATUS_OPTIONS = ["Booked", "Driver Assigned", "In Progress", "Completed", "Cancelled"]


@app.route("/")
def dashboard():
    data = get_dashboard_data()
    return render_template("dashboard.html", data=data, active_page="dashboard")


@app.route("/customers", methods=["GET"])
def customers():
    all_customers = view_customers()
    return render_template("customers.html", customers=all_customers, active_page="customers")


@app.route("/customers/add", methods=["POST"])
def customers_add():
    name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not phone:
        flash("Customer name and phone are required.", "error")
        return redirect(url_for("customers"))

    add_customer(name, phone, email)
    flash(f"{name} added to the customer book.", "success")
    return redirect(url_for("customers"))


@app.route("/trips", methods=["GET"])
def trips():
    all_trips = view_trips()
    all_customers = view_customers()
    trips_with_progress = []
    for trip in all_trips:
        trip_dict = dict(trip)
        trip_dict["progress"] = STATUS_PROGRESS.get(trip["status"], 0)
        trips_with_progress.append(trip_dict)
    return render_template(
        "trips.html",
        trips=trips_with_progress,
        customers=all_customers,
        status_options=STATUS_OPTIONS,
        active_page="trips",
    )


@app.route("/trips/add", methods=["POST"])
def trips_add():
    try:
        customer_id = int(request.form.get("customer_id"))
        fare = float(request.form.get("fare", 0))
        fuel_cost = float(request.form.get("fuel_cost", 0) or 0)
    except (TypeError, ValueError):
        flash("Customer, fare and fuel cost must be valid numbers.", "error")
        return redirect(url_for("trips"))

    pickup = request.form.get("pickup", "").strip()
    destination = request.form.get("destination", "").strip()
    vehicle = request.form.get("vehicle", "").strip()
    driver = request.form.get("driver", "").strip()
    payment_method = request.form.get("payment_method", "").strip()
    trip_date = request.form.get("trip_date", "").strip()

    if not pickup or not destination or not vehicle:
        flash("Pickup, destination and vehicle are required.", "error")
        return redirect(url_for("trips"))

    add_trip(
        customer_id, pickup, destination, vehicle, driver,
        fare, fuel_cost, payment_method, trip_date
    )
    flash(f"Trip booked: {pickup} → {destination}.", "success")
    return redirect(url_for("trips"))


@app.route("/trips/<int:trip_id>/status", methods=["POST"])
def trips_update_status(trip_id):
    new_status = request.form.get("status")
    if new_status not in STATUS_OPTIONS:
        flash("Invalid status.", "error")
        return redirect(url_for("trips"))

    update_trip_status(trip_id, new_status)
    flash(f"Trip #{trip_id} marked {new_status}.", "success")
    return redirect(url_for("trips"))


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, host="0.0.0.0", port=5000)
