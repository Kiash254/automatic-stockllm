import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("supermarket.db")

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Create tables for products, customers, sales, employees, and suppliers
tables_info = [
    """
    CREATE TABLE PRODUCTS (
        ID INTEGER PRIMARY KEY,
        NAME VARCHAR(50),
        CATEGORY VARCHAR(50),
        PRICE REAL,
        QUANTITY INTEGER
    );
    """,
    """
    CREATE TABLE CUSTOMERS (
        ID INTEGER PRIMARY KEY,
        NAME VARCHAR(50),
        EMAIL VARCHAR(50),
        PHONE VARCHAR(20),
        ADDRESS TEXT
    );
    """,
    """
    CREATE TABLE SALES (
        ID INTEGER PRIMARY KEY,
        CUSTOMER_ID INTEGER,
        PRODUCT_ID INTEGER,
        QUANTITY INTEGER,
        TOTAL REAL,
        DATE TEXT,
        FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(ID),
        FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS(ID)
    );
    """,
    """
    CREATE TABLE EMPLOYEES (
        ID INTEGER PRIMARY KEY,
        NAME VARCHAR(50),
        POSITION VARCHAR(50),
        SALARY REAL
    );
    """,
    """
    CREATE TABLE SUPPLIERS (
        ID INTEGER PRIMARY KEY,
        NAME VARCHAR(50),
        CONTACT_PERSON VARCHAR(50),
        PHONE VARCHAR(20),
        EMAIL VARCHAR(50),
        ADDRESS TEXT
    );
    """
]

for table_info in tables_info:
    cursor.execute(table_info)

# Insert 60 records into each table
products = [
    (i, f'Product {i}', 'Category', 1.99, 50) for i in range(1, 61)
]
customers = [
    (i, f'Customer {i}', f'customer{i}@example.com', '1234567890', 'Address') for i in range(1, 61)
]
sales = [
    (i, i % 60 + 1, i % 60 + 1, 1, 1.99, '2024-03-13') for i in range(1, 61)
]
employees = [
    (i, f'Employee {i}', 'Position', 1000.0) for i in range(1, 61)
]
suppliers = [
    (i, f'Supplier {i}', 'Contact Person', '1234567890', f'supplier{i}@example.com', 'Address') for i in range(1, 61)
]

cursor.executemany("INSERT INTO PRODUCTS VALUES (?, ?, ?, ?, ?)", products)
cursor.executemany("INSERT INTO CUSTOMERS VALUES (?, ?, ?, ?, ?)", customers)
cursor.executemany("INSERT INTO SALES VALUES (?, ?, ?, ?, ?, ?)", sales)
cursor.executemany("INSERT INTO EMPLOYEES VALUES (?, ?, ?, ?)", employees)
cursor.executemany("INSERT INTO SUPPLIERS VALUES (?, ?, ?, ?, ?, ?)", suppliers)

# Display the inserted records
print("The inserted records for PRODUCTS are:")
data = cursor.execute("""SELECT * FROM PRODUCTS""")
for row in data:
    print(row)

print("The inserted records for CUSTOMERS are:")
data = cursor.execute("""SELECT * FROM CUSTOMERS""")
for row in data:
    print(row)

print("The inserted records for SALES are:")
data = cursor.execute("""SELECT * FROM SALES""")
for row in data:
    print(row)

print("The inserted records for EMPLOYEES are:")
data = cursor.execute("""SELECT * FROM EMPLOYEES""")
for row in data:
    print(row)

print("The inserted records for SUPPLIERS are:")
data = cursor.execute("""SELECT * FROM SUPPLIERS""")
for row in data:
    print(row)

# Commit the transactions
connection.commit()
connection.close()
