from database import (
    create_tables,

    # Customer CRUD
    add_customer,
    view_customers,
    find_customer,
    update_customer,
    delete_customer,

    # Trip CRUD
    add_trip,
    view_trips,
    find_trip,
    update_trip_status,
    delete_trip
)

from analytics import (
    get_dashboard_data,
    get_total_profit,
    get_average_revenue_per_trip,
    get_completion_rate,
    get_cancellation_rate,
    get_active_rate,
    get_customer_rankings
)
