import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("my_insurance.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    bmi REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS InsurancePolicy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_name TEXT,
    premium REAL,
    coverage REAL,
    duration TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS CustomerPolicy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    policy_id INTEGER,
    start_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES Customer(id),
    FOREIGN KEY(policy_id) REFERENCES InsurancePolicy(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    policy_id INTEGER,
    claim_amount REAL,
    claim_date TEXT,
    status TEXT,
    FOREIGN KEY(customer_id) REFERENCES Customer(id),
    FOREIGN KEY(policy_id) REFERENCES InsurancePolicy(id)
)
""")

conn.commit()
conn.close()
print("Custom Insurance Database Created.")
