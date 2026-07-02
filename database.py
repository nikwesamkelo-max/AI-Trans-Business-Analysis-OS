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

            phone TEXT,

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
