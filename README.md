# SQL CLI Playground 🚀

## What is SQL CLI Playground? 🤔

SQL CLI Playground is a lightweight, interactive command-line tool that lets you:
- Create and modify SQL tables using Python syntax 🐍
- Execute SQL queries against these tables ⚡
- Visualize results in beautifully formatted tables 📊

Perfect for SQL practice, data exploration, and quick prototyping without the overhead of setting up a full database server.

## Features ✨

- **Python-Powered Table Manipulation** 💻 - Use familiar Python syntax to create and modify tables
- **Interactive SQL Shell** 🔍 - Run SQL queries directly from the command line
- **Beautiful Output** 🎨 - Results formatted with rich tables for easy reading
- **Command History** 📜 - Access previous commands and results
- **Schema Inspection** 📋 - Easily view table structures
- **No Setup Required** 🔧 - Works out of the box with in-memory tables
- **DataFrame Integration** 📊 - Access query results as pandas DataFrames

## Installation 📦

We support two installation methods:

### Method 1: Poetry (recommended) 🎵
- Quick setup via the provided script:
  ```bash
  bash project_setup.sh
  ```
- Or manual steps:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install poetry
  poetry install
  ```

### Method 2: pip-only (no Poetry) 🔄
> Alternative for users who do not wish to use Poetry.

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Usage 🏃‍♂️

### Run the CLI
```bash
poetry run sql-cli-playground
```
or if installed via pip-only:
```bash
sql-cli-playground
```

### Run tests
```bash
poetry run pytest
```
or if installed via pip-only:
```bash
pytest
```

## Quick Demo 🎬

```bash
poetry run sql-cli-playground
(tables: []) >> /create table1                                     # Create a new table
(tables: ['table1']) >> import numpy as np; table1['col1'] = np.random.randint(1, 50, 5)  # Add data using Python
(tables: ['table1']) >> table1['col2'] = np.random.rand(5) * 10    # Add another column
(tables: ['table1']) >>
SELECT col1, col2 FROM table1 LIMIT 3;                            # Run SQL query
# → nicely formatted table via rich
┌──────┬───────────┐
│ col1 │ col2      │
├──────┼───────────┤
│ 34   │ 4.823...  │
│ 12   │ 9.155...  │
│ 4    │ 0.567...  │
└──────┴───────────┘
[grey62]... 2 more rows[/]
(tables: ['table1']) >> _ # Access last SQL result DataFrame
# → Shows DataFrame representation
(tables: ['table1']) >> /schema table1                            # Inspect table schema
# → Shows PRAGMA table_info() output via rich
┌─────┬───────┬─────────┬─────────┬────────┬─────────┐
│ cid │ name  │ type    │ notnull │ dflt_value │ pk │
├─────┼───────┼─────────┼─────────┼────────┼─────────┤
│ 0   │ col1  │ INTEGER │ 0       │ <NA>       │ 0  │
│ 1   │ col2  │ REAL    │ 0       │ <NA>       │ 0  │
└─────┴───────┴─────────┴─────────┴────────┴─────────┘
(tables: ['table1']) >> /exit                                     # Exit the CLI
```

## Commands 🛠️

| Command | Description |
|---------|-------------|
| `/create tablename` | Create a new table |
| `/schema tablename` | View table schema |
| `_` | Access the last SQL query result |
| `/exit` or `/quit` | Exit the CLI |
| Any valid SQL | Execute SQL query |
| Any valid Python | Execute Python code to manipulate tables |

---

Happy SQL exploring! 🔎
