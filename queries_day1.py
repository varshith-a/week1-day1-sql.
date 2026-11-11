import sqlite3
import pandas as pd

# Read the CSV file
df = pd.read_csv("indian_sales_practice.csv")

# Put the data into a small SQL database (table name: sales)
conn = sqlite3.connect(":memory:")
df.to_sql("sales", conn, index=False)

# Query 1: show the first 5 rows
query = "SELECT * FROM sales LIMIT 5;"
print(pd.read_sql_query(query, conn))
# Query 2: only orders from Bengaluru
query = "SELECT order_id, city, sales FROM sales WHERE city = 'Bengaluru';"
print("Query 2")
print(pd.read_sql_query(query, conn))

# Query 3: Electronics orders with sales above 10000
query = "SELECT order_id, category, sales FROM sales WHERE category = 'Electronics' AND sales > 10000;"
print("Query 3")
print(pd.read_sql_query(query, conn))
# Query 4: OR (orders from Mumbai or Chennai)
query = "SELECT order_id, city, sales FROM sales WHERE city = 'Mumbai' OR city = 'Chennai';"
print("Query 4")
print(pd.read_sql_query(query, conn))

# Query 5: IN (orders from three states)
query = "SELECT order_id, state, sales FROM sales WHERE state IN ('Karnataka', 'Delhi', 'Telangana');"
print("Query 5")
print(pd.read_sql_query(query, conn))

# Query 6: BETWEEN (sales from 1000 to 5000)
query = "SELECT order_id, product, sales FROM sales WHERE sales BETWEEN 1000 AND 5000;"
print("Query 6")
print(pd.read_sql_query(query, conn))

# Query 7: LIKE (products that start with the letter P)
query = "SELECT order_id, product FROM sales WHERE product LIKE 'P%';"
print("Query 7")
print(pd.read_sql_query(query, conn))
# Query 8: NOT (all orders except the Consumer segment)
query = "SELECT order_id, segment, sales FROM sales WHERE NOT segment = 'Consumer';"
print("Query 8")
print(pd.read_sql_query(query, conn))

# Query 9: IS NULL (orders where profit is missing)
query = "SELECT order_id, profit FROM sales WHERE profit IS NULL;"
print("Query 9")
print(pd.read_sql_query(query, conn))

# Query 10: AND + OR together (South region, Furniture or Electronics)
query = "SELECT order_id, region, category, sales FROM sales WHERE region = 'South' AND (category = 'Furniture' OR category = 'Electronics');"
print("Query 10")
result = pd.read_sql_query(query, conn)
print(result)

# Export Query 10 to a CSV file
result.to_csv("query10_result.csv", index=False)
print("CSV exported: query10_result.csv")