from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from database import view_customers, add_customer, DatabaseError
from validators import validate_customer

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customers", methods=["GET"])
def index():
    try:
        all_customers = view_customers()
    except DatabaseError as e:
        current_app.logger.error("Failed to load customers: %s", e)
        flash("Couldn't load customers right now — please try again.", "error")
        all_customers = []
    return render_template("customers.html", customers=all_customers, active_page="customers")


@customers_bp.route("/customers/add", methods=["POST"])
def add():
    errors, cleaned = validate_customer(request.form)
    if errors:
        for msg in errors:
            flash(msg, "error")
        return redirect(url_for("customers.index"))

    try:
        success, error_message = add_customer(cleaned["customer_name"], cleaned["phone"], cleaned["email"])
    except DatabaseError as e:
        current_app.logger.error("Failed to add customer: %s", e)
        flash("Something went wrong saving that customer. Please try again.", "error")
        return redirect(url_for("customers.index"))

    if success:
        flash(f"{cleaned['customer_name']} added to the customer book.", "success")
    else:
        flash(error_message, "error")
    return redirect(url_for("customers.index"))
