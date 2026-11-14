import sqlite3
import pandas as pd

# Read the CSV file and put it into a small SQL database
sales_df = pd.read_csv("indian_sales_practice.csv")
conn = sqlite3.connect(":memory:")
sales_df.to_sql("sales", conn, index=False)

# Query 1: SUBQUERY - orders with sales above the average
query = """
SELECT order_id, city, sales
FROM sales
WHERE sales > (SELECT AVG(sales) FROM sales)
ORDER BY sales DESC
LIMIT 5;
"""
print("Query 1: top 5 orders above the average sales")
print(pd.read_sql_query(query, conn))
# Query 2: CORRELATED SUBQUERY - the top sale in each region
query = """
SELECT s1.order_id, s1.region, s1.city, s1.sales
FROM sales s1
WHERE s1.sales = (
    SELECT MAX(s2.sales)
    FROM sales s2
    WHERE s2.region = s1.region
)
ORDER BY s1.region, s1.order_id;
"""
print("Query 2: top sale in each region")
print(pd.read_sql_query(query, conn))

# Query 3: CORRELATED SUBQUERY - orders above the average of their OWN city
query = """
SELECT s1.order_id, s1.city, s1.sales
FROM sales s1
WHERE s1.sales > (
    SELECT AVG(s2.sales)
    FROM sales s2
    WHERE s2.city = s1.city
)
ORDER BY s1.sales DESC
LIMIT 5;
"""
print("Query 3: orders above their own city average")
print(pd.read_sql_query(query, conn))
# Query 4: CTE - the same job as Query 1 (orders above the average)
query = """
WITH avg_sales AS (
    SELECT AVG(sales) AS avg_value
    FROM sales
)
SELECT s.order_id, s.city, s.sales
FROM sales s
JOIN avg_sales a ON s.sales > a.avg_value
ORDER BY s.sales DESC
LIMIT 5;
"""
print("Query 4: CTE - orders above the average")
print(pd.read_sql_query(query, conn))

# Query 5: CTE - the same job as Query 2 (top sale in each region)
query = """
WITH region_max AS (
    SELECT region, MAX(sales) AS max_sales
    FROM sales
    GROUP BY region
)
SELECT s.order_id, s.region, s.city, s.sales
FROM sales s
JOIN region_max r ON s.region = r.region AND s.sales = r.max_sales
ORDER BY s.region, s.order_id;
"""
print("Query 5: CTE - top sale in each region")
print(pd.read_sql_query(query, conn))
# Query 6: CHAIN 2 CTEs - cities with total sales above the average city total
query = """
WITH city_totals AS (
    SELECT city, SUM(sales) AS total_sales
    FROM sales
    GROUP BY city
),
avg_city AS (
    SELECT AVG(total_sales) AS avg_total
    FROM city_totals
)
SELECT c.city,
       ROUND(c.total_sales, 2) AS total_sales,
       ROUND(a.avg_total, 2) AS avg_city_total
FROM city_totals c
JOIN avg_city a ON c.total_sales > a.avg_total
ORDER BY c.total_sales DESC;
"""
print("Query 6: chained CTEs")
print(pd.read_sql_query(query, conn))