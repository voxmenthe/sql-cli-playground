# SQL Puzzles for sql-cli-playground

Here are some SQL puzzles to practice your skills within the `sql-cli-playground` environment. For each puzzle, first run the provided Python code snippets in the CLI to set up the necessary tables. Then, write and execute the SQL query to solve the puzzle.

Give me some high-level approaches for how to solve this SQL puzzle (just the barest hint - DO NOT solve it for me).

---

## Puzzle 1: Simple Selection (Easy)

**Task:** Select the `name` and `species` of all pets from the `pets` table.

**Setup Code (Run in CLI):**

```python
# Run these lines one by one in the CLI
/create pets2
pets2['id'] = [1, 2, 3, 4, 5]
pets2['name'] = ['Buddy', 'Lucy', 'Max', 'Daisy', 'Charlie']
pets2['species'] = ['Dog', 'Cat', 'Dog', 'Dog', 'Cat']
pets2['age'] = [3, 5, 2, 7, 1]
```

**Expected Output:** A table showing only the `name` and `species` columns for all 5 pets.

DONE: SELECT name, species FROM pets;

---

## Puzzle 2: Filtering Data (Easy)

**Task:** Find the names of all dogs older than 3 years from the `pets` table.

**Setup Code:** (Use the `pets` table created in Puzzle 1)

**Expected Output:** A table showing the names 'Daisy'.

DONE: SELECT name FROM pets WHERE species = 'Dog' AND age > 3;

---

## Puzzle 3: Aggregation and Grouping (Medium)

**Task:** Calculate the average age for each pet species in the `pets` table.

**Setup Code:** (Use the `pets` table created in Puzzle 1)

**Expected Output:** A table showing each `species` and its corresponding average age (e.g., Dog: 4.0, Cat: 3.0).

DONE: SELECT species, AVG(age) FROM pets GROUP BY species;

---

## Puzzle 4: Simple Join (Medium)

**Task:** List the names of pets and the names of their owners.

**Setup Code (Run in CLI):**

```python
# Assumes 'pets' table exists from Puzzle 1
/create owners
owners['owner_id'] = [101, 102, 103, 104, 105]
owners['name'] = ['Alice', 'Bob', 'Carol', 'David', 'Eve']
owners['pet_id'] = [1, 2, 3, 4, 6] # Note: Pet ID 5 has no owner, Pet ID 6 doesn't exist in pets
```

**Expected Output:** A table showing pet names alongside their owner's name for pets 1 through 4. Buddy/Alice, Lucy/Bob, Max/Carol, Daisy/David.

DONE: SELECT p.name AS pet_name, o.name AS owner_name FROM pets p INNERJOIN owners o ON p.id = o.pet_id;

---

## Puzzle 5: Finding Max Value in Groups (Medium/Hard)

**Task:** Find the name and salary of the employee with the highest salary in each department.

**Setup Code (Run in CLI):**

```python
/create employees
employees['emp_id'] = [1, 2, 3, 4, 5, 6, 7]
employees['name'] = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace']
employees['department'] = ['HR', 'Engineering', 'Engineering', 'HR', 'Sales', 'Sales', 'Engineering']
employees['salary'] = [60000, 80000, 85000, 65000, 70000, 75000, 90000]
```

**Hint:** You might need `GROUP BY` and an aggregate function like `MAX()`, potentially in a subquery or using window functions if your SQLite version supports them well (`ROW_NUMBER()`).

**Expected Output:** A table showing the highest earner(s) from each department:
*   HR: David, 65000
*   Engineering: Grace, 90000
*   Sales: Frank, 75000

DONE: 
... SELECT department, MAX(salary) as max_sal FROM employees
... GROUP BY department)
...
... SELECT e.name, e.salary, e.department FROM employees e
... INNER JOIN MaxSalary ms
... ON e.department = ms.department
... AND e.salary = ms.max_sal;

or

... With RankedEmployees AS (
... SELECT name, salary, department,
... ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
... FROM employees)
... SELECT name, salary, department
... FROM RankedEmployees
... WHERE rn = 1;
---

## Puzzle 6: Self Join or Subquery (Hard)

**Task:** Find the names of employees who earn more than their managers. Assume direct managers are listed in a separate table.

**Setup Code (Run in CLI):**

```python
# Assumes 'employees' table exists from Puzzle 5
/create managers
managers['emp_id'] = [1, 2, 3, 5, 6, 7] # Alice, Bob, Charlie, Eve, Frank, Grace
managers['manager_id'] = [4, 7, 7, -1, 5, 2] # David, Grace, Grace, NULL (Top), Eve, Bob
# Map: Alice->David, Bob->Grace, Charlie->Grace, Eve->(None), Frank->Eve, Grace->Bob
```

**Hint:** You'll need to join the `employees` table with itself (self-join) or use a subquery to compare an employee's salary with their manager's salary obtained via the `managers` table. Handle the case where an employee might not have a manager (`manager_id` = -1 or similar).

**Expected Output:** A table showing employees who earn more than their manager. Based on the data:
*   Grace (90000) earns more than Bob (80000).
*   Bob (80000) does *not* earn more than Grace (90000).
*   Frank (75000) earns more than Eve (70000).

DONE: 
... SELECT
... e.name AS employee_name,
... e.salary AS employee_salary,
... mgr.name AS manager_name,
... mgr.salary AS manager_salary
... FROM employees e
... JOIN managers m
... ON e.emp_id = m.emp_id
... JOIN employees mgr
... ON m.manager_id = mgr.emp_id
... WHERE e.salary > mgr.salary;
---

## Puzzle 7: Outer Join (Medium)

**Task:** List all employees and their corresponding manager's name. Include employees who do not have a manager listed in the `managers` table.

**Setup Code:** (Use `employees` and `managers` tables from Puzzle 5 & 6)

**Hint:** How do you include rows from one table even when there's no matching row in the table you are joining it with?

**Expected Output:** A table showing each employee's name and their manager's name. Employees without managers (like Eve) should still appear, perhaps with a NULL value for the manager's name.

DONE:
... SELECT
... e.name as employee_name,
... mgr.name as manager_name
... FROM employees e
... LEFT JOIN managers m
... ON e.emp_id = m.emp_id
... LEFT JOIN employees mgr
... ON m.manager_id = mgr.emp_id;

---

## Puzzle 8: Conditional Aggregation (Medium)

**Task:** Count the number of employees in the 'Engineering' department versus the total number of employees in all *other* departments combined.

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** Think about how you can use functions like `COUNT` or `SUM` along with a condition (like an `IF` or `CASE` statement) inside the aggregation.

**Expected Output:** A table showing two counts, one for 'Engineering' employees and one for 'Other Departments'. (e.g., Engineering: 3, Other: 4)

DONE:
... SELECT
... COUNT(CASE WHEN department = 'Engineering' THEN 1 END) AS Engineering,
... COUNT(CASE WHEN department != 'Engineering' THEN 1 END) AS Other
... FROM employees;

---

## Puzzle 9: Working with Dates (Medium)

**Task:** Find employees hired in the year 2023.

**Setup Code (Run in CLI):**

```python
# Assumes 'employees' table exists from Puzzle 5
employees['hire_date'] = ['2022-05-10', '2023-01-15', '2023-08-20', '2022-11-01', '2024-02-28', '2023-06-10', '2022-03-15']
```

**Hint:** Most SQL dialects provide functions to extract parts of a date (like the year).

**Expected Output:** A table listing the names of employees hired in 2023 (Bob, Charlie, Frank).

DONE:
... SELECT name, strftime('%Y', hire_date) AS year
... FROM employees
... WHERE year = '2023';

---

## Puzzle 10: String Matching (Easy)

**Task:** Find all employees whose names start with the letter 'A'.

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** Look for SQL operators specifically designed for pattern matching in strings.

**Expected Output:** A table listing the employee(s) whose name starts with 'A' (Alice).

DONE:
... SELECT name
... FROM employees
... WHERE substr(name, 1, 1) = 'A';

---

## Puzzle 11: Multiple Joins (Medium)

**Task:** List the names of projects assigned to employees working in the 'Engineering' department.

**Setup Code (Run in CLI):**

```python
# Assumes 'employees' table exists from Puzzle 5
/create projects
projects['proj_id'] = ['P1', 'P2', 'P3', 'P4']
projects['proj_name'] = ['Website Redesign', 'Database Migration', 'Mobile App', 'Security Audit']

/create assignments
assignments['assign_id'] = [101, 102, 103, 104, 105, 106]
assignments['emp_id'] = [2, 3, 7, 1, 3, 5] # Bob, Charlie, Grace, Alice, Charlie, Eve
assignments['proj_id'] = ['P1', 'P1', 'P2', 'P3', 'P4', 'P3']
```

**Hint:** You'll need to link three tables together: employees to assignments, and assignments to projects.

**Expected Output:** A table listing the project names associated with 'Engineering' employees (Bob, Charlie, Grace). Expected projects: Website Redesign, Database Migration, Security Audit.

DONE:
... SELECT
... e.name, p.proj_name
... FROM employees e
... JOIN assignments a
... ON a.emp_id = e.emp_id
... JOIN projects p
... ON a.proj_id = p.proj_id
... WHERE e.department = 'Engineering';

---

## Puzzle 12: Finding Duplicates (Medium)

**Task:** Find all salary values that are paid to more than one employee.

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** How can you group rows based on a specific value and then count how many rows fall into each group? How do you filter these groups?

**Expected Output:** A table listing salary values that appear more than once. (In the sample data, no salary is duplicated, but the query should work if there were duplicates). If Alice also made 80000, the output should show 80000.

DONE:
... SELECT salary, COUNT(salary)
... from employees
... GROUP BY salary;
---

## Puzzle 13: Nth Highest Value (Hard)

**Task:** Find the name and salary of the employee with the 3rd highest salary. (Assume no ties for simplicity, or define how to handle ties).

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** Can you order the employees by salary and then somehow select only the row at a specific position? Think about subqueries or `LIMIT`/`OFFSET`.

**Expected Output:** A table showing the name and salary of the 3rd highest paid employee (Bob, 80000).

DONE:
... SELECT name, salary
... FROM employees
... ORDER BY salary DESC
... LIMIT 1 OFFSET 2;

... with ranked as (
... select name, salary, RANK() OVER (ORDER BY salary DESC) as sal_rank
... from employees)
... select name, salary
... from ranked
... where sal_rank = 3;
---

## Puzzle 14: Pivot Data (Hard)

**Task:** Display the total salary budget for each department, but with departments as columns rather than rows.

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** Similar to conditional aggregation, use `SUM` with conditions (e.g., `CASE`) to sum salaries only for specific departments, creating separate columns for each.

**Expected Output:** A single row table with columns like `HR_Total`, `Engineering_Total`, `Sales_Total`, showing the sum of salaries for each. (HR: 125000, Engineering: 255000, Sales: 145000)

---

## Puzzle 15: Set Operations (Easy)

**Task:** List the names of all employees who are in the 'HR' department *or* the 'Sales' department.

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** How do you combine the results of two separate `SELECT` statements into a single list?

**Expected Output:** A table listing the names of employees in HR or Sales (Alice, David, Eve, Frank).

---

## Puzzle 16: Correlated Subquery (Hard)

**Task:** For each employee, find the average salary of *their specific department*.

**Setup Code:** (Use `employees` table from Puzzle 5)

**Hint:** Can a subquery refer to values from the outer query that contains it? Use this to calculate the average salary only for the current employee's department within the subquery.

**Expected Output:** A table showing each employee's name, department, salary, and a column with the average salary for their department (e.g., Alice, HR, 60000, 62500; Bob, Engineering, 80000, 85000; etc.).

---

## Puzzle 17: Feature Engineering - Binning (Medium)

**Task:** Categorize customers into 'Low', 'Medium', or 'High' spenders based on their total purchase amount. Thresholds: Low < 100, Medium < 500, High >= 500.

**Setup Code (Run in CLI):**

```python
/create customers
customers['customer_id'] = [1, 2, 3, 4, 5, 6]
customers['name'] = ['Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Ava']

/create purchases
purchases['purchase_id'] = [101, 102, 103, 104, 105, 106, 107, 108]
purchases['customer_id'] = [1, 2, 1, 3, 4, 2, 5, 6]
purchases['amount'] = [50.0, 120.0, 30.0, 450.0, 600.0, 80.0, 25.0, 700.0]
```

**Hint:** You'll need to aggregate purchase amounts per customer first. Then, use a `CASE` statement to apply the category labels based on the total amount.

**Expected Output:** A table showing each customer's ID, name, total purchase amount, and their spending category ('Low', 'Medium', or 'High').

---

## Puzzle 18: Feature Engineering - Lag Features (Hard)

**Task:** For each product on each date, find the sales amount from the *previous* day. Assume dates are consecutive where data exists.

**Setup Code (Run in CLI):**

```python
/create daily_sales
daily_sales['sale_date'] = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-01', '2023-01-02', '2023-01-03']
daily_sales['product_id'] = [10, 10, 10, 20, 20, 20]
daily_sales['sales_amount'] = [100, 110, 105, 50, 55, 60]
# Convert date string to actual date type if needed by the specific SQL environment
# In sqlite-web or similar, date strings might work directly for comparisons
# If not, you might need: daily_sales['sale_date'] = pd.to_datetime(daily_sales['sale_date']) # before loading
```

**Hint:** Window functions like `LAG()` are ideal for this. You need to partition by the product and order by date to look back correctly. Handle the first day for each product where there's no previous day.

**Expected Output:** A table showing sale date, product ID, sales amount, and the previous day's sales amount (or NULL/0 for the first day).

---

## Puzzle 19: Data Cleaning - Identifying Missing Values (Easy)

**Task:** Find all rows in the `sensor_readings` table where the `temperature` reading is missing (NULL).

**Setup Code (Run in CLI):**

```python
/create sensor_readings
sensor_readings['reading_id'] = [1, 2, 3, 4, 5, 6]
sensor_readings['sensor_id'] = ['A', 'B', 'A', 'C', 'B', 'A']
sensor_readings['timestamp'] = ['2023-05-01 10:00', '2023-05-01 10:00', '2023-05-01 10:05', '2023-05-01 10:00', '2023-05-01 10:05', '2023-05-01 10:10']
sensor_readings['temperature'] = [25.5, 22.0, None, 30.1, None, 26.0] # Using Python's None for NULL
sensor_readings['humidity'] = [60, 65, 62, 55, 68, 61]
```

**Hint:** SQL has a specific operator to check if a value `IS NULL`.

**Expected Output:** A table showing the full rows (all columns) for readings where the temperature is NULL (reading_ids 3 and 5).

---

## Puzzle 20: Data Sampling (Medium)

**Task:** Select approximately 50% of the user sessions randomly from the `user_sessions` table.

**Setup Code (Run in CLI):**

```python
/create user_sessions
user_sessions['session_id'] = range(1, 21) # 20 sessions
user_sessions['user_id'] = [ (i % 5) + 1 for i in range(20)] # Users 1-5
user_sessions['duration_seconds'] = [ (i * 10) + 30 for i in range(20)]
```

**Hint:** Most SQL dialects have a function to generate random numbers (e.g., `RANDOM()` or `RAND()`). You can use this in an `ORDER BY` clause and `LIMIT` the result, or use it in a `WHERE` clause to filter rows probabilistically. The exact method might vary slightly based on the SQL flavor (SQLite's `RANDOM()` is common).

**Expected Output:** A table containing roughly half (around 10 rows) of the original `user_sessions` table, selected randomly. The exact rows will vary on each execution.

---

## Puzzle 21: A/B Testing Analysis - Basic Comparison (Medium)

**Task:** Calculate the conversion rate (percentage of users who made a purchase) for users in the 'Control' group versus the 'Treatment' group.

**Setup Code (Run in CLI):**

```python
/create experiment_users
experiment_users['user_id'] = range(1, 11) # 10 users
experiment_users['group_name'] = ['Control'] * 5 + ['Treatment'] * 5

/create user_actions
user_actions['action_id'] = range(101, 116) # 15 actions
user_actions['user_id'] = [1, 2, 6, 3, 7, 8, 1, 4, 9, 6, 2, 10, 5, 7, 3] # Some users repeat actions
user_actions['action_type'] = ['view', 'view', 'view', 'click', 'view', 'purchase', 'click', 'view', 'purchase', 'click', 'purchase', 'view', 'view', 'purchase', 'purchase']
```

**Hint:** First, identify which users made a purchase. Then, join this information with the experiment group assignments. Finally, aggregate counts per group (total users, converted users) and calculate the rate (converted / total * 100.0). Use `COUNT(DISTINCT user_id)` carefully.

**Expected Output:** A table showing two rows, one for 'Control' and one for 'Treatment', with their respective conversion rates. (Control: User 3 & 5 purchased? / 5 users. Treatment: User 6, 7, 8, 9 purchased? / 5 users).

---

## Puzzle 22: Time Series Analysis - Simple Moving Average (Hard)

**Task:** Calculate the 3-day moving average of website `visits` for the entire site.

**Setup Code (Run in CLI):**

```python
/create website_traffic
website_traffic['log_date'] = ['2023-03-01', '2023-03-02', '2023-03-03', '2023-03-04', '2023-03-05', '2023-03-06', '2023-03-07']
website_traffic['visits'] = [1000, 1100, 1050, 1200, 1150, 1300, 1250]
# Ensure log_date is treated as a date for ordering
```

**Hint:** This is a classic use case for window functions. You need `AVG(visits)` over a window defined by `ORDER BY log_date` that includes the current row and the 2 preceding rows (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`).

**Expected Output:** A table showing each date and the corresponding 3-day moving average of visits. The first two days will have averages based on fewer than 3 days.

---

## Puzzle 23: User Segmentation - RFM Prep (Medium/Hard)

**Task:** For each customer, calculate their total number of purchases (Frequency) and the total amount spent (Monetary Value). (Recency is harder without transaction dates, so we skip it here).

**Setup Code:** (Use `customers` and `purchases` tables from Puzzle 11)

**Hint:** You need to `GROUP BY` customer and use two different aggregate functions: `COUNT()` for frequency and `SUM()` for monetary value. Join with the `customers` table to get names.

**Expected Output:** A table showing `customer_id`, `name`, `Frequency` (count of purchases), and `Monetary` (sum of purchase amounts) for each customer.

---

## Puzzle 24: Anomaly Detection - Simple Thresholding (Medium)

**Task:** Identify users whose average session duration is more than 1.5 times the overall average session duration across all users.

**Setup Code:** (Use `user_sessions` table from Puzzle 14)

**Hint:** First, calculate the overall average duration. Then, calculate the average duration per user. Finally, select users whose average duration exceeds the overall average multiplied by 1.5. Subqueries or CTEs (Common Table Expressions) are helpful here.

**Expected Output:** A table listing the `user_id` and their average session duration for users identified as having anomalously long average sessions.

---

## Puzzle 25: Data Transformation - Finding Min/Max for Scaling (Easy)

**Task:** Find the minimum and maximum values for the `feature1` column in the `ml_data` table. This is often needed for Min-Max scaling: `(value - min) / (max - min)`.

**Setup Code (Run in CLI):**

```python
/create ml_data
ml_data['id'] = range(1, 8)
ml_data['feature1'] = [10.5, 12.1, 8.3, 15.0, 9.9, 11.2, 14.5]
ml_data['feature2'] = [100, 110, 95, 120, 105, 108, 115]
ml_data['label'] = [0, 1, 0, 1, 0, 1, 1]
```

**Hint:** Use the `MIN()` and `MAX()` aggregate functions. You don't need a `GROUP BY` if you want the overall min/max across the whole table.

**Expected Output:** A single row table showing the minimum and maximum values found in `feature1`. (Min: 8.3, Max: 15.0).

---

## Puzzle 26: Model Evaluation Prep - Confusion Matrix Counts (Hard)

**Task:** Given a table of actual labels and predicted labels, count the number of True Positives (TP), False Positives (FP), True Negatives (TN), and False Negatives (FN). Assume '1' is the positive class and '0' is the negative class.

**Setup Code (Run in CLI):**

```python
/create predictions
predictions['id'] = range(1, 11) # 10 predictions
predictions['actual_label'] = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
predictions['predicted_label'] = [1, 1, 0, 1, 0, 1, 1, 0, 0, 0]
```

**Hint:** This requires conditional aggregation. Use `SUM()` with `CASE` statements for each of the four conditions:
*   TP: actual = 1 AND predicted = 1
*   FP: actual = 0 AND predicted = 1
*   TN: actual = 0 AND predicted = 0
*   FN: actual = 1 AND predicted = 0

**Expected Output:** A single row table with four columns: TP, FP, TN, FN, showing the counts for each category based on the provided data.

---

## Puzzle 27: Handling Missing Values - Imputation (Medium)

**Task:** Replace missing `temperature` values in the `sensor_readings` table with the average temperature for the same sensor on the same day.

**Setup Code:** (Use `sensor_readings` table from Puzzle 19)

**Hint:** You'll need to calculate the average temperature per sensor per day first. Then, use this in an `UPDATE` statement or a `SELECT` with `COALESCE()` to replace missing values.

**Expected Output:** The modified `sensor_readings` table with missing `temperature` values replaced.

---

## Puzzle 28: Data Quality Check - Duplicate Rows (Easy)

**Task:** Identify and count duplicate rows in the `user_sessions` table.

**Setup Code:** (Use `user_sessions` table from Puzzle 14)

**Hint:** Use `COUNT(*)` with `GROUP BY` on all columns. Then, filter for groups with more than one row.

**Expected Output:** A table showing the duplicate rows and their counts.

---

## Puzzle 29: Data Normalization - Scaling (Medium)

**Task:** Scale the `feature1` and `feature2` columns in the `ml_data` table using Min-Max scaling.

**Setup Code:** (Use `ml_data` table from Puzzle 25)

**Hint:** Calculate the minimum and maximum for each feature. Then, apply the Min-Max scaling formula: `(value - min) / (max - min)`.

**Expected Output:** The `ml_data` table with `feature1` and `feature2` scaled between 0 and 1.

---

## Puzzle 30: Data Visualization Prep - Aggregating for Plotting (Medium)

**Task:** Prepare data for plotting the distribution of `feature1` values in the `ml_data` table by aggregating into bins.

**Setup Code:** (Use `ml_data` table from Puzzle 25)

**Hint:** Decide on a bin size, then use `GROUP BY` with a `CASE` statement to assign each value to a bin. Count the number of values in each bin.

**Expected Output:** A table showing the bins and their respective counts, ready for plotting.

---
