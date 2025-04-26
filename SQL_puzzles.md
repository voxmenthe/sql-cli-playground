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

