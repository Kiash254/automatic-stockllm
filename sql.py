import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("supermarket.db")

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Create a table for products
table_info = """
CREATE TABLE PRODUCTS (
    ID INTEGER PRIMARY KEY,
    NAME VARCHAR(50),
    CATEGORY VARCHAR(50),
    PRICE REAL,
    QUANTITY INTEGER
);
"""
cursor.execute(table_info)

# Insert sample product records
products = [
    (1, 'Apple', 'Fruits', 1.99, 50),
    (2, 'Milk', 'Dairy', 2.49, 100),
    (3, 'Bread', 'Bakery', 1.49, 75),
    (4, 'Chicken', 'Meat', 5.99, 30),
    (5, 'Rice', 'Grains', 3.99, 200),
    (6, 'Tomato', 'Vegetables', 0.99, 100),
    (7, 'Orange', 'Fruits', 0.79, 80),
    (8, 'Cheese', 'Dairy', 3.99, 50),
    (9, 'Cake', 'Bakery', 4.99, 20),
    (10, 'Beef', 'Meat', 8.99, 40),
    (11, 'Applesauce', 'Fruits', 2.99, 60),
    (12, 'Yogurt', 'Dairy', 1.99, 70),
    (13, 'Croissant', 'Bakery', 2.99, 40),
    (14, 'Salmon', 'Seafood', 9.99, 25),
    (15, 'Pasta', 'Grains', 1.99, 150),
    (16, 'Lettuce', 'Vegetables', 0.49, 120),
    (17, 'Grapes', 'Fruits', 2.99, 90),
    (18, 'Ice Cream', 'Dairy', 4.99, 30),
    (19, 'Donut', 'Bakery', 1.99, 50),
    (20, 'Pork', 'Meat', 7.99, 35),

]

cursor.executemany("INSERT INTO PRODUCTS VALUES (?, ?, ?, ?, ?)", products)

# Display the inserted records
print("The inserted records are:")
data = cursor.execute("""SELECT * FROM PRODUCTS""")
for row in data:
    print(row)

# Commit the transactions
connection.commit()
connection.close()
