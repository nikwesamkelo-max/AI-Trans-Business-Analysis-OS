from flask import Blueprint, render_template, current_app

from analytics import get_dashboard_data
from database import DatabaseError

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    try:
        data = get_dashboard_data()
    except DatabaseError as e:
        current_app.logger.error("Dashboard failed to load: %s", e)
        data = None
    return render_template("dashboard.html", data=data, active_page="dashboard")
