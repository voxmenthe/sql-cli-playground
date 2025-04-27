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

