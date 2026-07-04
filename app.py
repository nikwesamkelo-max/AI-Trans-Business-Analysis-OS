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


#TRIP FEATURES

def add_trip_ui():

    print("\n=== BOOK A TRIP ===")

    customers = view_customers()

    if not customers:
        print("No customers found. Add a customer first.")
        return

    print("\nAvailable Customers")
    print("-" * 40)

    for customer in customers:
        print(f"{customer['customer_id']} - {customer['customer_name']}")

    customer_id = int(input("\nCustomer ID: "))

    pickup = input("Pickup Location: ")
    destination = input("Destination: ")
    vehicle = input("Vehicle: ")
    driver = input("Driver: ")

    fare = float(input("Fare: "))
    fuel_cost = float(input("Fuel Cost: "))

    payment_method = input("Payment Method: ")

    trip_date = input("Trip Date (YYYY-MM-DD): ")

    add_trip(
        customer_id,
        pickup,
        destination,
        vehicle,
        driver,
        fare,
        fuel_cost,
        payment_method,
        trip_date
        )


def view_trips_ui():

    print("\n=== TRIP LIST ===")

    trips = view_trips()

    if not trips:
        print("No trips found.")
        return

    for trip in trips:

        print("-" * 40)

        print(f"Trip ID: {trip['trip_id']}")
        print(f"Customer: {trip['customer_name']}")
        print(f"Pickup: {trip['pickup']}")
        print(f"Destination: {trip['destination']}")
        print(f"Vehicle: {trip['vehicle']}")
        print(f"Driver: {trip['driver']}")
        print(f"Fare: R{trip['fare']:.2f}")
        print(f"Fuel Cost: R{trip['fuel_cost']:.2f}")
        print(f"Payment: {trip['payment_method']}")
        print(f"Status: {trip['status']}")
        print(f"Date: {trip['trip_date']}")


def find_trip_ui():

    trip_id = int(input("\nEnter Trip ID: "))

    trip = find_trip(trip_id)

    if not trip:
        print("Trip not found.")
        return

    print("-" * 40)
    print(f"Trip ID: {trip['trip_id']}")
    print(f"Customer ID: {trip['customer_id']}")
    print(f"Pickup: {trip['pickup']}")
    print(f"Destination: {trip['destination']}")
    print(f"Status: {trip['status']}")


def update_trip_status_ui():

    trip_id = int(input("\nEnter Trip ID: "))

    print("\nChoose New Status")
    print("1. Booked")
    print("2. Driver Assigned")
    print("3. In Progress")
    print("4. Completed")
    print("5. Cancelled")

    choice = input("\nSelect Status: ")

    status_map = {
        "1": "Booked",
        "2": "Driver Assigned",
        "3": "In Progress",
        "4": "Completed",
        "5": "Cancelled"
    }

    if choice not in status_map:
        print("Invalid status selected.")
        return

    update_trip_status(trip_id, status_map[choice])


def delete_trip_ui():

    trip_id = int(input("\nEnter Trip ID: "))

    delete_trip(trip_id)
    

#DASHBOARD FEATURES

def show_dashboard():

    print("\n========== BUSINESS DASHBOARD ==========\n")

    dashboard = get_dashboard_data()

    print(f"Total Trips        : {dashboard['total_trips']}")
    print(f"Completed Trips    : {dashboard['completed_trips']}")
    print(f"Active Trips       : {dashboard['active_trips']}")
    print(f"Cancelled Trips    : {dashboard['cancelled_trips']}")

    print("-" * 40)

    print(f"Total Revenue      : R{dashboard['total_revenue']:.2f}")
    print(f"Fuel Cost          : R{dashboard['fuel_cost']:.2f}")
    print(f"Total Profit       : R{dashboard['profit']:.2f}")

    print("-" * 40)

    print(f"Average Revenue    : R{dashboard['average_revenue']:.2f}")

    print(f"Completion Rate    : {dashboard['completion_rate']}%")
    print(f"Cancellation Rate  : {dashboard['cancellation_rate']}%")
    print(f"Active Rate        : {dashboard['active_rate']}%")
    

def show_revenue_report():

    print("\n========== REVENUE REPORT ==========\n")

    print(f"Total Revenue           : R{get_dashboard_data()['total_revenue']:.2f}")

    print(f"Fuel Cost               : R{get_dashboard_data()['fuel_cost']:.2f}")

    print(f"Total Profit            : R{get_total_profit():.2f}")

    print(f"Average Revenue/Trip    : R{get_average_revenue_per_trip():.2f}") 


def show_customer_rankings():

    print("\n========== TOP CUSTOMERS ==========\n")

    customers = get_customer_rankings()

    if not customers:
        print("No customer data available.")
        return

    for customer in customers:

        print(
            f"{customer['customer_name']} "
            f"- {customer['total_trips']} trips"
        )
        
#MAIN PROGRAM 

def main():

    create_tables()

    while True:

        choice = main_menu()


if choice == "1":

            while True:

                customer_choice = customer_menu()

                if customer_choice == "1":
                    add_customer_ui()

                elif customer_choice == "2":
                    view_customers_ui()

                elif customer_choice == "3":
                    find_customer_ui()

                elif customer_choice == "4":
                    update_customer_ui()

                elif customer_choice == "5":
                    delete_customer_ui()

                elif customer_choice == "0":
                    break

                else:
                    print("Invalid option.")
