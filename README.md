### Installation

We support two installation methods:

#### Method 1: Poetry (recommended)
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

#### Method 2: pip-only (no Poetry)
> Alternative for users who do not wish to use Poetry.

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Run the CLI
```bash
poetry run sql-cli-playground
```
# or if installed via pip-only
sql-cli-playground

### Run tests
```bash
poetry run pytest
```
# or if installed via pip-only
pytest

### Quick demo

```bash
poetry run sql-cli-playground
(tables: []) >> /create table1
(tables: ['table1']) >> import numpy as np; table1['col1'] = np.random.randint(1, 50, 5)
(tables: ['table1']) >> table1['col2'] = np.random.rand(5) * 10
(tables: ['table1']) >>
SELECT col1, col2 FROM table1 LIMIT 3;
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
(tables: ['table1']) >> /schema table1
# → Shows PRAGMA table_info() output via rich
┌─────┬───────┬─────────┬─────────┬────────┬─────────┐
│ cid │ name  │ type    │ notnull │ dflt_value │ pk │
├─────┼───────┼─────────┼─────────┼────────┼─────────┤
│ 0   │ col1  │ INTEGER │ 0       │ <NA>       │ 0  │
│ 1   │ col2  │ REAL    │ 0       │ <NA>       │ 0  │
└─────┴───────┴─────────┴─────────┴────────┴─────────┘
(tables: ['table1']) >> /exit
```
