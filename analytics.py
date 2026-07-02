from database import (
    get_total_trips,
    get_completed_trips,
    get_active_trips,
    get_cancelled_trips,
    get_total_revenue,
    get_total_fuel_cost,
    get_top_customers
)

=========================
REVENUE ANALYTICS
==========================

 def get_total_profit():

    revenue = get_total_revenue()

    fuel_cost = get_total_fuel_cost()

    return revenue - fuel_cost


def get_average_revenue_per_trip():

    completed = get_completed_trips()

    if completed == 0:
        return 0

    revenue = get_total_revenue()

    return round(revenue / completed, 2)

==========================
TRIP ANALYTICS
==========================

    def get_completion_rate():

    total = get_total_trips()

    if total == 0:
        return 0

    completed = get_completed_trips()

    return round((completed / total) * 100, 2)


def get_cancellation_rate():

    total = get_total_trips()

    if total == 0:
        return 0

    cancelled = get_cancelled_trips()

    return round((cancelled / total) * 100, 2)


def get_active_rate():

    total = get_total_trips()

    if total == 0:
        return 0

    active = get_active_trips()

    return round((active / total) * 100, 2)

==========================
CUSTOMER ANALYTICS
==========================

    def get_customer_rankings():

    return get_top_customers()


=========================
BUSINESS DASHBOARD

def get_dashboard_data():

    return {

        "total_trips": get_total_trips(),

        "completed_trips": get_completed_trips(),

        "active_trips": get_active_trips(),

        "cancelled_trips": get_cancelled_trips(),

        "total_revenue": get_total_revenue(),

        "fuel_cost": get_total_fuel_cost(),

        "profit": get_total_profit(),

        "average_revenue": get_average_revenue_per_trip(),

        "completion_rate": get_completion_rate(),

        "cancellation_rate": get_cancellation_rate(),

        "active_rate": get_active_rate(),

        "top_customers": get_customer_rankings()

}
