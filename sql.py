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

products = [
    (1, 'Apple', 'Fruits', 1.99, 50),
    (2, 'Milk', 'Dairy', 2.49, 50),
    (3, 'Bread', 'Bakery', 1.49, 50),
    (4, 'Chicken', 'Meat', 5.99, 50),
    (5, 'Rice', 'Grains', 3.99, 50),
    (6, 'Tomato', 'Vegetables', 0.99, 50),
    (7, 'Orange', 'Fruits', 0.79, 50),
    (8, 'Cheese', 'Dairy', 3.99, 50),
    (9, 'Cake', 'Bakery', 4.99, 50),
    (10, 'Beef', 'Meat', 8.99, 50),
    (11, 'Applesauce', 'Fruits', 2.99, 50),
    (12, 'Yogurt', 'Dairy', 1.99, 50),
    (13, 'Croissant', 'Bakery', 2.99, 50),
    (14, 'Salmon', 'Seafood', 9.99, 50),
    (15, 'Pasta', 'Grains', 1.99, 50),
    (16, 'Lettuce', 'Vegetables', 0.49, 50),
    (17, 'Grapes', 'Fruits', 2.99, 50),
    (18, 'Ice Cream', 'Dairy', 4.99, 50),
    (19, 'Donut', 'Bakery', 1.99, 50),
    (20, 'Pork', 'Meat', 7.99, 50),
    (21, 'Banana', 'Fruits', 0.59, 50),
    (22, 'Eggs', 'Dairy', 2.99, 50),
    (23, 'Baguette', 'Bakery', 2.49, 50),
    (24, 'Turkey', 'Meat', 6.99, 50),
    (25, 'Quinoa', 'Grains', 4.99, 50),
    
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
