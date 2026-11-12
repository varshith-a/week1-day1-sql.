import sqlite3
import pandas as pd

# Read the 3 CSV files
sales_df = pd.read_csv("indian_sales_practice.csv")
managers_df = pd.read_csv("city_managers.csv")
employees_df = pd.read_csv("employees.csv")

# Put them into a small SQL database
conn = sqlite3.connect(":memory:")
sales_df.to_sql("sales", conn, index=False)
managers_df.to_sql("city_managers", conn, index=False)
employees_df.to_sql("employees", conn, index=False)

# Query 1: INNER JOIN (only cities that exist in BOTH tables)
query = """
SELECT s.order_id, s.city, s.sales, m.manager_name
FROM sales s
INNER JOIN city_managers m ON s.city = m.city
LIMIT 10;
"""
print("Query 1: INNER JOIN")
print(pd.read_sql_query(query, conn))
# Query 2: LEFT JOIN (all sales rows, even if the city has no manager)
query = """
SELECT DISTINCT s.city, m.manager_name
FROM sales s
LEFT JOIN city_managers m ON s.city = m.city
ORDER BY s.city;
"""
print("Query 2: LEFT JOIN")
print(pd.read_sql_query(query, conn))

# Query 3: find the cities that have NO manager
query = """
SELECT DISTINCT s.city
FROM sales s
LEFT JOIN city_managers m ON s.city = m.city
WHERE m.manager_name IS NULL;
"""
print("Query 3: cities without a manager")
print(pd.read_sql_query(query, conn))
# Query 4: RIGHT JOIN (all managers, even if their city has no sales)
query = """
SELECT DISTINCT m.city, m.manager_name
FROM sales s
RIGHT JOIN city_managers m ON s.city = m.city
WHERE s.order_id IS NULL;
"""
print("Query 4: RIGHT JOIN - managers whose city has no sales")
print(pd.read_sql_query(query, conn))

# Query 5: FULL OUTER JOIN (everything from both tables)
query = """
SELECT DISTINCT s.city AS sales_city, m.city AS manager_city, m.manager_name
FROM sales s
FULL OUTER JOIN city_managers m ON s.city = m.city
ORDER BY manager_city;
"""
print("Query 5: FULL OUTER JOIN")
print(pd.read_sql_query(query, conn))
# Query 6: count the rows BEFORE the join
query = "SELECT COUNT(*) AS manager_rows FROM city_managers;"
print("Query 6: rows in city_managers")
print(pd.read_sql_query(query, conn))

# Query 7: join manager (one) to sales (many) - rows get repeated
query = """
SELECT COUNT(*) AS rows_after_join
FROM city_managers m
INNER JOIN sales s ON m.city = s.city;
"""
print("Query 7: rows after join (duplicates!)")
print(pd.read_sql_query(query, conn))

# Query 8: FIX - summarise sales first, then join
query = """
SELECT m.city, m.manager_name, t.total_sales
FROM city_managers m
INNER JOIN (
    SELECT city, SUM(sales) AS total_sales
    FROM sales
    GROUP BY city
) t ON m.city = t.city;
"""
print("Query 8: fixed - one row per city")
print(pd.read_sql_query(query, conn))
# Query 9: SELF JOIN (each employee with their boss)
query = """
SELECT e.emp_name AS employee, e.role, b.emp_name AS boss
FROM employees e
LEFT JOIN employees b ON e.manager_id = b.emp_id;
"""
print("Query 9: SELF JOIN")
print(pd.read_sql_query(query, conn))

# Query 10: only the people who report to Anita Rao
query = """
SELECT e.emp_name AS employee, e.role, b.emp_name AS boss
FROM employees e
INNER JOIN employees b ON e.manager_id = b.emp_id
WHERE b.emp_name = 'Anita Rao';
"""
print("Query 10: reports to Anita Rao")
print(pd.read_sql_query(query, conn))