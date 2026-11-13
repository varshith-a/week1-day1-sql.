import sqlite3
import pandas as pd

# Read the CSV file and put it into a small SQL database
sales_df = pd.read_csv("indian_sales_practice.csv")
conn = sqlite3.connect(":memory:")
sales_df.to_sql("sales", conn, index=False)

# Query 1: all 5 aggregate functions on the whole table
query = """
SELECT COUNT(*) AS total_orders,
       SUM(sales) AS total_sales,
       ROUND(AVG(sales), 2) AS avg_sales,
       MAX(sales) AS max_sale,
       MIN(sales) AS min_sale
FROM sales;
"""
print("Query 1: overall summary")
print(pd.read_sql_query(query, conn))
# Query 2: total sales for each region
query = """
SELECT region, COUNT(*) AS orders, ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;
"""
print("Query 2: sales by region")
print(pd.read_sql_query(query, conn))

# Query 3: average profit for each category
query = """
SELECT category, ROUND(AVG(profit), 2) AS avg_profit
FROM sales
GROUP BY category;
"""
print("Query 3: average profit by category")
print(pd.read_sql_query(query, conn))

# Query 4: total sales for each month (first 5 months)
query = """
SELECT strftime('%Y-%m', order_date) AS month, ROUND(SUM(sales), 2) AS monthly_sales
FROM sales
GROUP BY month
ORDER BY month
LIMIT 5;
"""
print("Query 4: sales by month")
print(pd.read_sql_query(query, conn))
# Query 5: only cities with total sales above 500000
query = """
SELECT city, ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY city
HAVING SUM(sales) > 500000
ORDER BY total_sales DESC;
"""
print("Query 5: cities with total sales above 500000")
print(pd.read_sql_query(query, conn))

# Query 6: WHERE and HAVING together
query = """
SELECT category, COUNT(*) AS orders, ROUND(SUM(sales), 2) AS total_sales
FROM sales
WHERE region = 'South'
GROUP BY category
HAVING COUNT(*) > 30;
"""
print("Query 6: South region, categories with more than 30 orders")
print(pd.read_sql_query(query, conn))
# Query 7: best and worst profit for each segment
query = """
SELECT segment, MAX(profit) AS best_profit, MIN(profit) AS worst_profit
FROM sales
GROUP BY segment;
"""
print("Query 7: MAX and MIN profit by segment")
print(pd.read_sql_query(query, conn))

# Query 8: GROUP BY two columns (region and category)
query = """
SELECT region, category, ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY region, category
ORDER BY region, total_sales DESC;
"""
print("Query 8: sales by region and category")
print(pd.read_sql_query(query, conn))

# Query 9: WINDOW FUNCTION (keeps every row and adds the region total)
query = """
SELECT order_id, region, sales,
       ROUND(SUM(sales) OVER (PARTITION BY region), 2) AS region_total
FROM sales
ORDER BY order_id
LIMIT 5;
"""
print("Query 9: window function")
print(pd.read_sql_query(query, conn))