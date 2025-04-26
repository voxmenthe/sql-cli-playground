from src.router import classify, MetaCommand, SqlBlock, PythonStmt
from src.manager import TableManager  # Needed if testing meta commands that use it
import sqlite3  # Needed if testing meta commands that use it
import pandas as pd  # Needed if testing meta commands that return DataFrames
import pytest  # For fixtures or raising exceptions

# Minimal fixture for tests needing a manager
@pytest.fixture
def table_manager():
    conn = sqlite3.connect(":memory:")
    yield TableManager(conn)
    conn.close()


def test_classify():
    assert isinstance(classify("/list"), MetaCommand)
    assert isinstance(classify("  SELECT 1;  "), SqlBlock)
    assert classify("  SELECT 1;  ").sql == "SELECT 1;"  # Check stripping
    assert isinstance(classify("x = 2"), PythonStmt)
    assert classify("x = 2").code == "x = 2"  # Check stripping
    assert isinstance(classify(""), PythonStmt)  # Empty input is Python no-op


def test_meta_help(table_manager):
    cmd = classify("/help")
    assert isinstance(cmd, MetaCommand)
    output = cmd.execute(table_manager)
    assert isinstance(output, str)
    assert "/create" in output
    assert "/load" in output
    assert "/save" in output
    assert "/export" in output
    assert "/list" in output
    assert "/schema" in output
    assert "/exit" in output


def test_meta_create_list(table_manager):
    # Create
    cmd_create = classify("/create my_table")
    assert isinstance(cmd_create, MetaCommand)
    result = cmd_create.execute(table_manager)
    assert result is None  # Create returns nothing
    assert "my_table" in table_manager.tables
    assert isinstance(table_manager.tables["my_table"], pd.DataFrame)

    # List
    cmd_list = classify("/list")
    assert isinstance(cmd_list, MetaCommand)
    result = cmd_list.execute(table_manager)
    assert result == ["my_table"]

    # Test create error (already exists)
    with pytest.raises(ValueError, match="already exists"):
        classify("/create my_table").execute(table_manager)

    # Test create error (invalid name)
    with pytest.raises(ValueError, match="Invalid table name"):
        classify("/create 1invalid").execute(table_manager)


def test_meta_schema(table_manager):
    # Test schema on non-existent table
    with pytest.raises(ValueError, match="not found"):
        classify("/schema no_such_table").execute(table_manager)

    # Create a table first
    classify("/create tbl_for_schema").execute(table_manager)
    table_manager.tables["tbl_for_schema"]["colA"] = [1, 2]
    table_manager.tables["tbl_for_schema"]["colB"] = ["a", "b"]
    table_manager.push_all()  # Push to DB

    cmd_schema = classify("/schema tbl_for_schema")
    assert isinstance(cmd_schema, MetaCommand)
    df_schema = cmd_schema.execute(table_manager)

    assert isinstance(df_schema, pd.DataFrame)
    assert list(df_schema.columns) == ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']
    assert df_schema['name'].tolist() == ['colA', 'colB']
    # SQLite types might vary slightly based on pandas version / data
    assert df_schema['type'].tolist() == ['INTEGER', 'TEXT']

# Add more tests for /load, /save, /export, /exit as needed
# Remember to handle file operations appropriately (e.g., using tmp_path fixture) 