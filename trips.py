from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from database import view_trips, view_customers, add_trip, update_trip_status, DatabaseError
from validators import validate_trip, validate_status

trips_bp = Blueprint("trips", __name__)

STATUS_PROGRESS = {
    "Booked": 5,
    "Driver Assigned": 30,
    "In Progress": 65,
    "Completed": 100,
    "Cancelled": 0,
}

STATUS_OPTIONS = list(STATUS_PROGRESS.keys())


@trips_bp.route("/trips", methods=["GET"])
def index():
    try:
        all_trips = view_trips()
        all_customers = view_customers()
    except DatabaseError as e:
        current_app.logger.error("Failed to load trips: %s", e)
        flash("Couldn't load trips right now — please try again.", "error")
        all_trips, all_customers = [], []

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


@trips_bp.route("/trips/add", methods=["POST"])
def add():
    errors, cleaned = validate_trip(request.form)
    if errors:
        for msg in errors:
            flash(msg, "error")
        return redirect(url_for("trips.index"))

    try:
        add_trip(
            cleaned["customer_id"], cleaned["pickup"], cleaned["destination"],
            cleaned["vehicle"], cleaned["driver"], cleaned["fare"], cleaned["fuel_cost"],
            cleaned["payment_method"], cleaned["trip_date"]
        )
    except DatabaseError as e:
        current_app.logger.error("Failed to add trip: %s", e)
        flash("Something went wrong booking that trip. Please try again.", "error")
        return redirect(url_for("trips.index"))

    flash(f"Trip booked: {cleaned['pickup']} → {cleaned['destination']}.", "success")
    return redirect(url_for("trips.index"))


@trips_bp.route("/trips/<int:trip_id>/status", methods=["POST"])
def update_status(trip_id):
    new_status = request.form.get("status")
    errors = validate_status(new_status, STATUS_OPTIONS)
    if errors:
        for msg in errors:
            flash(msg, "error")
        return redirect(url_for("trips.index"))

    try:
        update_trip_status(trip_id, new_status)
    except DatabaseError as e:
        current_app.logger.error("Failed to update trip #%s: %s", trip_id, e)
        flash("Couldn't update that trip's status. Please try again.", "error")
        return redirect(url_for("trips.index"))

    flash(f"Trip #{trip_id} marked {new_status}.", "success")
    return redirect(url_for("trips.index"))
