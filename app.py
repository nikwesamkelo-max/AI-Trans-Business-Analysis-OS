# ==========================
# CUSTOMER FUNCTIONS
# ==========================

from database import (
    add_customer,
    view_customers,
    find_customer,
    update_customer,
    delete_customer
)

# ==========================
# TRIP FUNCTIONS
# ==========================

from database import (
    add_trip,
    view_trips,
    find_trip,
    update_trip_status,
    delete_trip
)

# ==========================
# ANALYTICS
# ==========================

from analytics import (
    get_dashboard_data,
    get_total_profit,
    get_completion_rate,
    get_cancellation_rate,
    get_active_rate,
    get_average_revenue_per_trip,
    get_customer_rankings
)
