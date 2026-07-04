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

# ==========================
# MENU FUNCTIONS
# ==========================

def main_menu():

    print("\n" + "=" * 40)
    print(" TRANSPORT AI BUSINESS OS ")
    print("=" * 40)

    print("1. Customer Management")
    print("2. Trip Management")
    print("3. Business Dashboard")
    print("0. Exit")

    return input("\nSelect an option: ")


def customer_menu():

    print("\n--- CUSTOMER MANAGEMENT ---")

    print("1. Add Customer")
    print("2. View Customers")
    print("3. Find Customer")
    print("4. Update Customer")
    print("5. Delete Customer")
    print("0. Back")

    return input("\nSelect an option: ")


def trip_menu():

    print("\n--- TRIP MANAGEMENT ---")

    print("1. Add Trip")
    print("2. View Trips")
    print("3. Find Trip")
    print("4. Update Trip Status")
    print("5. Delete Trip")
    print("0. Back")

    return input("\nSelect an option: ")
    
    
def dashboard_menu():

    print("\n--- BUSINESS DASHBOARD ---")

    print("1. Business Summary")
    print("2. Revenue Report")
    print("3. Customer Rankings")
    print("0. Back")

    return input("\nSelect an option: ")


#CUSTOMER FEATURES

def add_customer_ui():

    print("\n=== ADD CUSTOMER ===")

    customer_name = input("Customer Name: ")
    phone = input("Phone Number: ")
    email = input("Email: ")

    add_customer(customer_name, phone, email)


def view_customers_ui():

    print("\n=== CUSTOMER LIST ===")

    customers = view_customers()

    if not customers:
        print("No customers found.")
        return

    for customer in customers:

        print("-" * 40)

        print(f"ID: {customer['customer_id']}")
        print(f"Name: {customer['customer_name']}")
        print(f"Phone: {customer['phone']}")
        print(f"Email: {customer['email']}")


def find_customer_ui():

    name = input("\nEnter customer name: ")

    customers = find_customer(name)

    if not customers:
        print("Customer not found.")
        return

    for customer in customers:

        print("-" * 40)

        print(f"ID: {customer['customer_id']}")
        print(f"Name: {customer['customer_name']}")
        print(f"Phone: {customer['phone']}")
        print(f"Email: {customer['email']}")


def update_customer_ui():

    customer_id = int(input("\nCustomer ID: "))

    phone = input("New Phone: ")

    email = input("New Email: ")

    update_customer(customer_id, phone, email)


def delete_customer_ui():

    customer_id = int(input("\nCustomer ID: "))

    delete_customer(customer_id)
