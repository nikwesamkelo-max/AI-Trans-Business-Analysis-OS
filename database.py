import sqlite3

DATABASE_NAME = "data/business.db"


# ==========================
# DATABASE CONNECTION
# ==========================

def connect():

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================
# DATABASE SETUP
# ==========================

def create_tables():

    conn = connect()
    cursor = conn.cursor()

    # --------------------------
    # Customers Table
    # --------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (

            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_name TEXT NOT NULL,

            phone TEXT UNIQUE,

            email TEXT,

            created_at TEXT

        )
    """)

    # --------------------------
    # Trips Table
    # --------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (

            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id INTEGER NOT NULL,

            pickup TEXT NOT NULL,

            destination TEXT NOT NULL,

            vehicle TEXT NOT NULL,

            driver TEXT,

            fare REAL NOT NULL,

            fuel_cost REAL DEFAULT 0,

            payment_method TEXT,

            status TEXT DEFAULT 'Booked',

            trip_date TEXT,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)

        )
    """)

    conn.commit()
    conn.close()

    print("✅ Database Version 2.0 Ready")

# ==========================
# CUSTOMER CRUD
# ==========================

def add_customer(customer_name, phone, email):

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO customers (
                customer_name,
                phone,
                email,
                created_at
            )
            VALUES (?, ?, ?, DATE('now'))
        """, (
            customer_name,
            phone,
            email
        ))

        conn.commit()
        print("✅ Customer added successfully.")

    except sqlite3.IntegrityError:
        print("❌ A customer with this phone number already exists.")

    finally:
        conn.close()
        

def view_customers():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM customers
        ORDER BY customer_name
    """)

    customers = cursor.fetchall()

    conn.close()

    return customers


def find_customer(customer_name):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM customers
        WHERE customer_name LIKE ?
    """, (f"%{customer_name}%",))

    customer = cursor.fetchall()

    conn.close()

    return customer


def update_customer(customer_id, phone, email):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE customers
        SET phone = ?,
            email = ?
        WHERE customer_id = ?
    """, (
        phone,
        email,
        customer_id
    ))

    conn.commit()
    conn.close()

    print("✅ Customer updated successfully.")


def delete_customer(customer_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM customers
        WHERE customer_id = ?
    """, (customer_id,))

    conn.commit()
    conn.close()

    print("✅ Customer deleted successfully.")


# ==========================
# TRIP CRUD
# ==========================

def add_trip(
    customer_id,
    pickup,
    destination,
    vehicle,
    driver,
    fare,
    fuel_cost,
    payment_method,
    trip_date
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trips (
            customer_id,
            pickup,
            destination,
            vehicle,
            driver,
            fare,
            fuel_cost,
            payment_method,
            status,
            trip_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_id,
        pickup,
        destination,
        vehicle,
        driver,
        fare,
        fuel_cost,
        payment_method,
        "Booked",
        trip_date
    ))

    conn.commit()
    conn.close()

    print("✅ Trip booked successfully.")


def view_trips():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            trips.trip_id,
            customers.customer_name,
            pickup,
            destination,
            vehicle,
            driver,
            fare,
            fuel_cost,
            payment_method,
            status,
            trip_date
        FROM trips
        JOIN customers
        ON trips.customer_id = customers.customer_id
        ORDER BY trip_date DESC
    """)

    trips = cursor.fetchall()

    conn.close()

    return trips


def find_trip(trip_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM trips
        WHERE trip_id = ?
    """, (trip_id,))

    trip = cursor.fetchone()

    conn.close()

    return trip


def update_trip_status(trip_id, new_status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE trips
        SET status = ?
        WHERE trip_id = ?
    """, (
        new_status,
        trip_id
    ))

    conn.commit()
    conn.close()

    print("✅ Trip status updated successfully.")
    
    
def delete_trip(trip_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM trips
        WHERE trip_id = ?
    """, (trip_id,))

    conn.commit()
    conn.close()

    print("✅ Trip deleted successfully.")


# ==========================
# DATABASE QUERY FUNCTIONS
# ==========================


def get_total_trips():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM trips
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_completed_trips():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM trips
        WHERE status = 'Completed'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total
