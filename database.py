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
