# SQL Puzzle Solutions

## Puzzle 1: Simple Selection (Easy)
```sql
SELECT name, species FROM pets;
```

## Puzzle 2: Filtering Data (Easy)
```sql
SELECT name FROM pets WHERE species = 'Dog' AND age > 3;
```

## Puzzle 3: Aggregation and Grouping (Medium)
```sql
SELECT species, AVG(age) FROM pets GROUP BY species;
```

## Puzzle 4: Simple Join (Medium)
```sql
SELECT p.name AS pet_name, o.name AS owner_name
FROM pets p
INNER JOIN owners o ON p.id = o.pet_id;
```

## Puzzle 5: Finding Max Value in Groups (Medium/Hard)
```sql
-- Method 1: Subquery join
SELECT e.name, e.salary, e.department
FROM employees e
JOIN (
  SELECT department, MAX(salary) AS max_sal
  FROM employees
  GROUP BY department
) ms ON e.department = ms.department AND e.salary = ms.max_sal;

-- Method 2: Window function
WITH RankedEmployees AS (
  SELECT name, salary, department,
         ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT name, salary, department
FROM RankedEmployees
WHERE rn = 1;
```

## Puzzle 6: Self Join or Subquery (Hard)
```sql
SELECT e.name AS employee_name,
       e.salary AS employee_salary,
       mgr.name AS manager_name,
       mgr.salary AS manager_salary
FROM employees e
JOIN managers m ON e.emp_id = m.emp_id
JOIN employees mgr ON m.manager_id = mgr.emp_id
WHERE e.salary > mgr.salary;
```

## Puzzle 7: Outer Join (Medium)
```sql
SELECT e.name AS employee_name,
       mgr.name AS manager_name
FROM employees e
LEFT JOIN managers m ON e.emp_id = m.emp_id
LEFT JOIN employees mgr ON m.manager_id = mgr.emp_id;
```

## Puzzle 8: Conditional Aggregation (Medium)
```sql
SELECT
  COUNT(CASE WHEN department = 'Engineering' THEN 1 END) AS Engineering,
  COUNT(CASE WHEN department != 'Engineering' THEN 1 END) AS Other
FROM employees;
```

## Puzzle 9: Working with Dates (Medium)
```sql
SELECT name
FROM employees
WHERE strftime('%Y', hire_date) = '2023';
```

## Puzzle 10: String Matching (Easy)
```sql
SELECT name
FROM employees
WHERE substr(name, 1, 1) = 'A';
```

## Puzzle 11: Multiple Joins (Medium)
```sql
SELECT e.name, p.proj_name
FROM employees e
JOIN assignments a ON a.emp_id = e.emp_id
JOIN projects p ON a.proj_id = p.proj_id
WHERE e.department = 'Engineering';
```

## Puzzle 12: Finding Duplicates (Medium)
```sql
SELECT name, salary
FROM employees
GROUP BY name, salary
HAVING COUNT(*) > 1;
```

## Puzzle 13: Nth Highest Value (Hard)
```sql
SELECT name, salary
FROM employees
WHERE salary = (
  SELECT salary
  FROM employees
  ORDER BY salary DESC
  LIMIT 1 OFFSET 2
);
```
```sql
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
```

## Puzzle 14: Pivot Data (Hard)
```sql
SELECT
  SUM(CASE WHEN department = 'HR' THEN salary ELSE 0 END) AS HR_Total,
  SUM(CASE WHEN department = 'Engineering' THEN salary ELSE 0 END) AS Engineering_Total,
  SUM(CASE WHEN department = 'Sales' THEN salary ELSE 0 END) AS Sales_Total
FROM employees;
```

## Puzzle 15: Set Operations (Easy)
```sql
SELECT name
FROM employees
WHERE department = 'HR'
UNION
SELECT name
FROM employees
WHERE department = 'Sales';
```

## Puzzle 16: Correlated Subquery (Hard)
```sql
SELECT e.name, e.department, e.salary,
       (SELECT AVG(salary) FROM employees WHERE department = e.department) AS avg_dept_salary
FROM employees e;
```

```sql
... WITH davg AS (
... SELECT department, AVG(salary) AS dept_avg
FROM employees
GROUP BY department)
SELECT e.name, e.department, e.salary, dept_avg
FROM employees e
LEFT JOIN davg
ON e.department = davg.department;
```

## Puzzle 17: Feature Engineering - Binning (Medium)


```sql
SELECT c.customer_id, c.name,
       SUM(p.amount) AS total_purchases,
       CASE
         WHEN SUM(p.amount) < 100 THEN 'Low'
         WHEN SUM(p.amount) < 500 THEN 'Medium'
         ELSE 'High'
       END AS spending_category
FROM customers c
LEFT JOIN purchases p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.name;
```

```sql
WITH spend AS (
  SELECT customer_id, SUM(amount) AS amtsum
  FROM purchases
  GROUP BY customer_id
)

SELECT c.customer_id, c.name, spend.amtsum,
(CASE 
 WHEN spend.amtsum < 100 THEN 'Low'
 WHEN spend.amtsum < 500 THEN 'Medium'
 ELSE 'High'
 END) AS category
FROM customers c
JOIN spend ON c.customer_id = spend.customer_id;
```

```sql
WITH spend AS (
  SELECT customer_id, SUM(amount) AS amtsum
  FROM purchases
  GROUP BY customer_id
)
SELECT c.customer_id, c.name, spend.amtsum,
(CASE 
  WHEN spend.amtsum < 100 THEN 'Low'
  WHEN spend.amtsum < 500 THEN 'Medium'
  ELSE 'High'
END) AS category
FROM customers c
JOIN spend
ON c.customer_id = spend.customer_id;
```

## Puzzle 18: Window Functions (Hard)

```sql
SELECT 
  sale_date,
  product_id,
  sales_amount,
  LAG(sales_amount) OVER (PARTITION BY product_id ORDER BY sale_date) AS prev_day_sales
FROM daily_sales;
```

## Puzzle 19: Data Cleaning - Identifying Missing Values (Easy)

```sql
SELECT * FROM sensor_readings WHERE temperature IS NULL;
```

## Puzzle 20: Data Sampling (Medium)

```sql
SELECT * FROM user_sessions ORDER BY RANDOM() LIMIT 10;
```

```sql
SELECT * FROM user_sessions
ORDER BY RANDOM()
LIMIT (SELECT COUNT(*)/2 FROM user_sessions);
```

## Puzzle 21: A/B Testing Analysis - Basic Comparison (Medium)

```sql
WITH purchasers AS (
  SELECT DISTINCT user_id
  FROM user_actions
  WHERE action_type = 'purchase'
)
SELECT
  eu.group_name,
  100.0
    * SUM(CASE WHEN p.user_id IS NOT NULL THEN 1 ELSE 0 END)
    / COUNT(*) AS conversion_rate
FROM experiment_users eu
LEFT JOIN purchasers p
  ON eu.user_id = p.user_id
GROUP BY eu.group_name
ORDER BY eu.group_name;
```

```sql
WITH purchasers AS (
  SELECT user_id
  FROM user_actions
  WHERE action_type = 'purchase'
),
ac AS (
  SELECT
    eu.group_name,
    COUNT(pu.user_id)       AS purchase_count,
    COUNT(eu.user_id)       AS total_users
  FROM experiment_users eu
  LEFT JOIN purchasers pu
    ON eu.user_id = pu.user_id
  GROUP BY eu.group_name
)
SELECT
  (SELECT purchase_count * 100.0 / total_users
   FROM ac
   WHERE group_name = 'Control')    AS control_conversion,
  (SELECT purchase_count * 100.0 / total_users
   FROM ac
   WHERE group_name = 'Treatment')  AS treatment_conversion;
```

## Puzzle 22: Time Series Analysis - Simple Moving Average (Hard)

```sql
SELECT log_date, visits, AVG(visits) OVER (
  ORDER BY log_date
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS running_3p
FROM website_traffic;
```

## Puzzle 23: User Segmentation - RFM Prep (Medium/Hard)

```sql
WITH agg AS (
  SELECT customer_id, COUNT(customer_id) AS frequency, SUM(amount) AS monetary
  FROM purchases
  GROUP BY customer_id)
SELECT c.customer_id, c.name, frequency, monetary
FROM customers c
JOIN agg ON c.customer_id = agg.customer_id;
```
```sql
SELECT
  c.customer_id,
  c.name,
  COUNT(p.purchase_id)    AS Frequency,
  COALESCE(SUM(p.amount), 0) AS Monetary
FROM customers AS c
LEFT JOIN purchases AS p
  ON c.customer_id = p.customer_id
GROUP BY
  c.customer_id,
  c.name;
```

## Puzzle 24: Anomaly Detection - Simple Thresholding (Medium)

```sql
WITH avg_duration AS (
  SELECT AVG(duration_seconds) AS avg_duration
  FROM user_sessions
)
SELECT user_id, AVG(duration_seconds) AS avg_user_duration
FROM user_sessions
GROUP BY user_id
HAVING AVG(duration_seconds) > (
  SELECT avg_duration * 1.5
  FROM avg_duration
);
```

```sql
WITH user_duration AS (
  SELECT user_id, AVG(duration_seconds) AS user_avg_duration,
  (SELECT AVG(duration_seconds) FROM user_sessions) AS ttl_avg_duration
  FROM user_sessions
  GROUP BY user_id
)
SELECT * FROM user_duration
WHERE user_avg_duration > ttl_avg_duration * 1.5;
```

## Puzzle 25: Data Transformation - Finding Min/Max for Scaling (Easy)

```sql
SELECT MIN(feature1) AS min_feature1, MAX(feature1) AS max_feature1
FROM ml_data;
```

And for follow-up to get the scaled feature:
```sql
WITH mm AS (
  SELECT
    MIN(feature1) AS min1,
    MAX(feature1) AS max1
  FROM ml_data
)
SELECT
  md.id,
  md.feature1,
  (md.feature1 - mm.min1)  /  (mm.max1 - mm.min1)  AS scaled_feature1
FROM ml_data AS md
CROSS JOIN mm;
```

## Puzzle 26: Model Evaluation Prep - Confusion Matrix Counts (Hard)

```sql
SELECT
  SUM(CASE WHEN actual_label = 1 AND predicted_label = 1 THEN 1 ELSE 0 END) AS TP,
  SUM(CASE WHEN actual_label = 0 AND predicted_label = 1 THEN 1 ELSE 0 END) AS FP,
  SUM(CASE WHEN actual_label = 0 AND predicted_label = 0 THEN 1 ELSE 0 END) AS TN,
  SUM(CASE WHEN actual_label = 1 AND predicted_label = 0 THEN 1 ELSE 0 END) AS FN
FROM predictions;
```

ELSE is optional in this particular case since null values are skipped
```sql
SELECT
  SUM(CASE WHEN actual_label = 1 and predicted_label = 1 THEN 1 END) AS TP,
  SUM(CASE WHEN actual_label = 0 and predicted_label = 1 THEN 1 END) AS FP,
  SUM(CASE WHEN actual_label = 0 and predicted_label = 0 THEN 1 END) AS TN,
  SUM(CASE WHEN actual_label = 1 and predicted_label = 0 THEN 1 END) AS FN
FROM predictions;
```

## Puzzle 27: Handling Missing Values - Imputation (Medium)

```sql
WITH averages AS (
  SELECT sensor_id, DATE(timestamp) AS day,
  COALESCE(AVG(temperature), (SELECT AVG(temperature) FROM sensors2)) AS imputed_temperature
  FROM sensors2
  GROUP BY sensor_id, day)
SELECT s.reading_id, s.sensor_id, s.timestamp, s.humidity,
COALESCE(s.temperature, a.imputed_temperature) AS temperature
FROM sensors2 s
LEFT JOIN averages a
ON s.sensor_id = a.sensor_id AND DATE(s.timestamp) = a.day;
```

Or update in place:
```sql
UPDATE sensors2
SET temperature = (
  SELECT COALESCE(AVG(temperature), (SELECT AVG(temperature) FROM sensors2))
  FROM sensors2 t
  WHERE t.sensor_id = sensors2.sensor_id
    AND DATE(t.timestamp) = DATE(sensors2.timestamp)
)
WHERE temperature IS NULL;
```

## Puzzle 28: Data Quality Check - Duplicate Rows (Easy)

```sql
SELECT *
FROM (
  SELECT 
    *,
    COUNT(*) OVER (PARTITION BY user_id, duration_seconds) as ct
  FROM user_sessions
) t
WHERE ct > 1;
```

## Puzzle 29: Data Normalization - Scaling (Medium)

```sql
WITH mm AS (
  SELECT
    MAX(feature1) as max1,
    MIN(feature1) as min1,
    MAX(feature2) as max2,
    MIN(feature2) as min2
  FROM ml_data
)
SELECT ml.id, ml.feature1, ml.feature2, ml.label,
(feature1 - mm.min1) * 1.0 / NULLIF(mm.max1 - mm.min1, 0) AS feature1_scaled, -- needed to avoid int/int tructation and division by zero
(feature2 - mm.min2) * 1.0 / NULLIF(mm.max2 - mm.min2, 0) AS feature2_scaled -- needed to avoid int/int tructation and division by zero
FROM ml_data ml
CROSS JOIN mm;
```

## Puzzle 30: Data Visualization Prep - Aggregating for Plotting (Medium)

```sql
SELECT id, feature1,
  CASE
    WHEN feature1 < 10 THEN 'bin1'
    WHEN feature1 < 13 THEN 'bin2'
    ELSE 'bin3' END AS bin,
  COUNT(*) as cnt
FROM ml_data
GROUP BY bin
ORDER BY bin;
```

## Puzzle 31: Sales Rep Ranking (Medium)

```sql
WITH ttl AS (
  SELECT
    rep_id, SUM(amount) AS total_sales
  FROM sales
  GROUP BY rep_id
)
SELECT rep_id, total_sales,
DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM ttl;
```

## Puzzle 32: Cumulative Monthly Revenue (Medium)

```sql
SELECT month, amount AS revenue,
SUM(amount) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING) AS cumulative_revenue
FROM sales_series;
```

```sql
SELECT amount AS revenue,
SUM(amount) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM sales_series;
```

## Puzzle 33: Top N Employees by Department (Medium)

```sql
WITH rnk AS (
  SELECT emp_id,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
  FROM employees2
)
SELECT e.name, e.department, e.salary, rnk.salary_rank
FROM employees2 e
JOIN rnk ON e.emp_id = rnk.emp_id
WHERE rnk.salary_rank <=2
ORDER BY department, salary_rank;
```

## Puzzle 34: Employee-Manager Self-Join (Easy)

```sql
SELECT
  e.emp_id, e.name AS employee_name, m2.name AS manager_name
FROM employees e
JOIN managers AS mgr
ON e.emp_id = mgr.emp_id
LEFT JOIN employees m2
ON mgr.manager_id = m2.emp_id;
```

## Puzzle 35: Organizational Hierarchy (Hard)

```sql
WITH RECURSIVE emp_mgr(emp_id, employee_name, manager_id, manager_chain) AS (
  -- anchor: every employee, start with empty TEXT chain
  SELECT
    e.emp_id,
    e.name,
    m.manager_id,
    '' 
  FROM employees2 e
  LEFT JOIN managers2 m
    ON e.emp_id = m.emp_id

  UNION ALL

  -- recurse: look up next manager, append name
  SELECT
    em.emp_id,
    em.employee_name,
    m2.manager_id,
    CASE
      WHEN em.manager_chain = '' 
        THEN mgr.name
      ELSE em.manager_chain || ' > ' || mgr.name
    END
  FROM emp_mgr em
  JOIN employees2 mgr
    ON em.manager_id = mgr.emp_id
  LEFT JOIN managers2 m2
    ON mgr.emp_id = m2.emp_id
)
SELECT
  emp_id,
  employee_name,
  manager_chain
FROM emp_mgr
WHERE manager_id IS NULL
ORDER BY emp_id;
```

## Puzzle 36: Customers Without Purchases (Easy)

```sql
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN purchases p
ON c.customer_id = p.customer_id
WHERE p.purchase_id IS NULL;
```

## Puzzle 37: Common Products (Easy)

```sql
SELECT product_id FROM product_sales
INTERSECT
SELECT product_id FROM returns;
```

## Puzzle 38: Monthly Sales Pivot (Medium)

```sql
SELECT product_id,
SUM(CASE WHEN month = '2023-01' THEN quantity ELSE 0 END) AS jan_sales,
SUM(CASE WHEN month = '2023-02' THEN quantity ELSE 0 END) AS feb_sales,
SUM(CASE WHEN month = '2023-03' THEN quantity ELSE 0 END) AS mar_sales,
SUM(CASE WHEN month = '2023-04' THEN quantity ELSE 0 END) AS apr_sales,
SUM(CASE WHEN month = '2023-05' THEN quantity ELSE 0 END) AS may_sales,
SUM(CASE WHEN month = '2023-06' THEN quantity ELSE 0 END) AS jun_sales
FROM product_sales2
GROUP BY product_id;
```

## Puzzle 39: Survey Data Unpivot (Medium)

```sql
SELECT response_id, 'q1' AS question, q1 AS answer FROM survey
UNION
SELECT response_id, 'q2' AS question, q2 AS answer FROM survey
UNION
SELECT response_id, 'q3' AS question, q3 AS answer FROM survey;
```

## Puzzle 40: JSON Data Extraction (Medium)

```sql
SELECT
  JSON_EXTRACT(data, '$.user.id') AS user_id,
  JSON_EXTRACT(data, '$.order.total') AS order_total
FROM json_data;
```

## Puzzle 41: Full-Text Search (Medium)

```sql
SELECT article_id, content
FROM articles
WHERE content LIKE '%database%';
```

## Puzzle 42: Moving Average Excluding Current Row (Hard)

```sql
SELECT reading_id, value,
AVG(value) OVER (ORDER BY reading_id ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS moving_avg
FROM measurements;
```

## Puzzle 43: Top Percentile Employees (Medium)

```sql
WITH dists AS (
  SELECT emp_id, name, salary,
  PERCENT_RANK() OVER (ORDER BY salary) as salrank,
  CUME_DIST() OVER (ORDER BY salary) as saldist
  FROM employees2
)
SELECT * from dists
WHERE salrank >= 0.9 OR saldist >= 0.9;
```

## Puzzle 44: Conditional Aggregation by Status (Easy)

```sql
SELECT status, COUNT(status) as ct
FROM order_status
GROUP BY status;
```

```sql
SELECT
  status,
  SUM(CASE WHEN status = 'Shipped' THEN 1 ELSE 0 END) AS shipped_count,
  SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending_count,
  SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_count
FROM order_status
GROUP BY status;
```

## Puzzle 45: Latest Order Per Customer (Hard)

```sql
WITH temp AS (
  SELECT
    p.customer_id, c.name, MAX(p.order_date) as most_recent
  FROM purchases p
  LEFT JOIN customers c
  ON c.customer_id = p.customer_id
  GROUP BY p.customer_id
)
SELECT t.customer_id, t.name AS customer_name, p2.purchase_id AS order_id, t.most_recent
FROM temp t
LEFT JOIN purchases p2
ON p2.customer_id = t.customer_id
AND t.most_recent = p2.order_date;
```

## Puzzle 46: Geospatial Distance Filter (Hard)

too hard but here's a thought:

```sql
-- reference point
PRAGMA foreign_keys = OFF;
WITH params AS (
  SELECT
    40.7128 AS ref_lat,    -- your ref latitude
    -74.0060 AS ref_lon,   -- your ref longitude
    10.0    AS max_km      -- 10 km radius
),
haversine AS (
  SELECT
    l.id,
    l.lat,
    l.lon,
    -- convert degrees to radians: deg * PI()/180
    2 * 6371.0 *
    ASIN(
      SQRT(
        POWER(
          SIN(((l.lat - p.ref_lat) * PI()/180) / 2)
        ,2)
      + COS(p.ref_lat * PI()/180)
        * COS(l.lat      * PI()/180)
        * POWER(
            SIN(((l.lon - p.ref_lon) * PI()/180) / 2)
          ,2
          )
      )
    ) AS dist_km
  FROM locations AS l
  CROSS JOIN params AS p
)
SELECT id, lat, lon, ROUND(dist_km,3) AS distance_km
FROM haversine
WHERE dist_km <= (SELECT max_km FROM params)
ORDER BY dist_km;
```

## Puzzle 47: Inactive Customers (Easy)

```sql
SELECT customer_id, last_login
FROM customers
WHERE julianday(CURRENT_DATE) - julianday(last_login) > 30;
```

```sql
SELECT * FROM customers
WHERE julianday('now') - julianday(last_login) > 30;
```


## Puzzle 48: Data Masking (Medium)

```sql
SELECT user_id, SUBSTR(ssn, 1, 3) || SUBSTR(ssn,8,11) as masked_ssn
FROM users_with_PII;
```

## Puzzle 49: Dense Ranking Scores (Medium)

```sql
SELECT player_id, score, DENSE_RANK() OVER (ORDER BY score DESC) as player_rank
FROM scores;
```

## Puzzle 50: Net Sales Calculation with CTEs (Hard)

```sql
WITH merged AS (
  SELECT ps.product_id, ps.quantity, COALESCE(r.quantity,0) AS returns
  FROM product_sales ps
  LEFT JOIN returns r
  ON ps.product_id = r.product_id
)
SELECT product_id, quantity - returns AS net_sales
FROM merged;
```


## Puzzle 51: Get counts of unique values for each column (Easy)

# rubric only - not working code:
```sql
SELECT column_name, COUNT(DISTINCT column_value) AS unique_count
FROM employees

GROUP BY column_name;
```

```sql
SELECT
  col_name,
  COUNT(DISTINCT col_value) AS uniq_count
FROM (
  SELECT
    'name'       AS col_name,
    name         AS col_value
  FROM employees

  UNION ALL

  SELECT
    'department' AS col_name,
    department   AS col_value
  FROM employees

  UNION ALL

  SELECT
    'salary' AS col_name,
    salary   AS col_value
  FROM employees  
) t
GROUP BY col_name;
```




## Puzzle 52: Given a table with columns a, b, and c, find the number of non-null values in each column

```sql
SELECT COUNT(sensor_id), COUNT(temperature), COUNT(humidity)
FROM sensor_readings;
```

## Puzzle 53: Differences between tables (Easy)

```sql
SELECT COUNT(*) AS count_only_in_C
FROM C
LEFT JOIN D ON C.id_col = D.id_col
WHERE D.id_col IS NULL;

SELECT COUNT(*) AS count_only_in_D
FROM D
LEFT JOIN C ON D.id_col = C.id_col
WHERE C.id_col IS NULL;
```

```sql
SELECT
  (SELECT COUNT(*) 
   FROM C
   LEFT JOIN D ON C.id_col = D.id_col
   WHERE D.id_col IS NULL)  AS only_in_C,
  (SELECT COUNT(*) 
   FROM D
   LEFT JOIN C ON D.id_col = C.id_col
   WHERE C.id_col IS NULL)  AS only_in_D;
```

## Puzzle 54: Imputation

```sql
WITH ai AS (
  SELECT education, AVG(income) AS avg_income
  FROM imputation_table
  GROUP BY education
)
SELECT t.id, t.education,
COALESCE(t.income, ai.avg_income) AS imputed_income
FROM imputation_table t
LEFT JOIN ai
ON t.education = ai.education;
```

```sql
SELECT
  id,
  education,
  COALESCE(income,
    AVG(income) OVER (PARTITION BY education)
  ) AS imputed_income
FROM imputation_table;
```

OR to add a fallback imputed value using the global average:
```sql
SELECT
  id,
  education,
  COALESCE(income,
    AVG(income) OVER (PARTITION BY education),
    AVG(income) OVER () -- global average
  ) AS imputed_income
FROM imputation_table;
```
