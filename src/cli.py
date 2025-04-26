"""
sql-cli-playground.cli
=================
REPL front-end with multiline editing that auto-switches
between Python and SQL, plus `/meta` commands.
"""

from __future__ import annotations

import sqlite3
import sys
from typing import Dict, Any

import numpy as np
import pandas as pd
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.table import Table
from pathlib import Path  # Import Path

from .manager import TableManager
from .router import classify, MetaCommand, SqlBlock, PythonStmt

console = Console()
# Expand the tilde in the history file path
HISTORY_FILE = Path("~/.sqlplayground_history").expanduser()
HISTORY = FileHistory(str(HISTORY_FILE)) # Pass the expanded path string

# Define the temporary directory path relative to this file
TEMP_TABLE_DIR = Path(__file__).parent / "TEMP_TABLES"

def _build_completer(tbl_mgr: TableManager) -> WordCompleter:
    words = set(tbl_mgr.tables.keys()) | {
        "SELECT", "FROM", "WHERE", "LIMIT", "INSERT", "UPDATE",
        "CREATE", "DROP", "DELETE"}
    words |= set(dir(np)) | set(dir(pd))
    return WordCompleter(list(words), ignore_case=True)


def _render_df(df: pd.DataFrame | None) -> None:
    if df is None or df.empty:
        console.print("[grey50]No results.[/]")
        return
    table = Table(show_header=True, header_style="bold cyan")
    for col in df.columns:
        table.add_column(str(col))
    for _, row in df.head(50).iterrows():          # cap preview
        table.add_row(*map(lambda x: str(x)[:40], row))
    console.print(table)
    if len(df) > 50:
        console.print(f"[grey62]... {len(df) - 50} more rows[/]")


def main() -> None:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    tables = TableManager(conn, TEMP_TABLE_DIR)

    # --- Add custom key bindings ---
    kb = KeyBindings()
    # Use Meta+Enter (Esc -> Enter or Alt+Enter)
    @kb.add('escape', 'enter')
    # Ctrl+Enter ('c-enter') is not reliably recognized.
    # Ctrl+S ('c-s') is another option if Meta+Enter is not preferred.
    def _(event):
        """Submit the input when Meta+Enter is pressed."""
        event.current_buffer.validate_and_handle()

    # Add a key binding for 'zz' to submit
    @kb.add('z', 'z')
    def _zz(event):
        """Submit the input when 'zz' is pressed."""
        event.current_buffer.validate_and_handle()
    # -----------------------------

    psession = PromptSession(history=HISTORY, completer=_build_completer(tables),
                             multiline=True,
                             prompt_continuation="... ",
                             key_bindings=kb) # Pass bindings to session

    banner = "[italic cyan]SQL-playground — mix Python & SQL.  /help for commands[/]"
    console.print(banner)

    # Start with core modules + empty tables dict, update as tables are added/removed
    globals_ns: Dict[str, Any] = {"np": np, "pd": pd, **tables.tables}

    while True:
        prompt = f"(tables: {list(tables.tables)}) >> "
        try:
            # with patch_stdout(): # Removed for testing
            text = psession.prompt(prompt)
        except KeyboardInterrupt:
            console.print("\n[bold]Interrupted. Use /exit or Ctrl-D to quit.[/]")
            continue # Go back to prompt
        except EOFError:
            console.print("\n[bold]Bye![/]")
            sys.exit(0)

        block = classify(text)

        # -- META ----------------------------------------------------------------
        if isinstance(block, MetaCommand):
            try:
                out = block.execute(tables)
                if isinstance(out, pd.DataFrame):
                    _render_df(out)
                elif out is not None: # Could be list of tables or help string
                    console.print(out)
                # Update globals and completer *only if* tables changed
                globals_ns.update(tables.tables) # Cheaper than checking, just update
                psession.completer = _build_completer(tables)
            except (ValueError, FileNotFoundError, sqlite3.Error) as e:
                console.print(f"[red]Error: {e}[/]")
            except SystemExit:
                # --- Save tables to TEMP_TABLE_DIR on exit ---
                console.print(f"[grey50]Saving tables to {TEMP_TABLE_DIR}...[/]")
                try:
                    tables.save_all_to_temp(TEMP_TABLE_DIR)
                    console.print(f"[grey50]Saved {len(tables.tables)} table(s).[/]")
                except Exception as e:
                    console.print(f"[red]Error saving tables: {e}[/]")
                # ----------------------------------------------
                console.print("\n[bold]Bye![/]")
                sys.exit(0)
            except Exception as e: # Catch unexpected errors
                 console.print(f"[bold red]Unexpected Error:[/]\n[red]{type(e).__name__}: {e}[/]")
                 console.print_exception(max_frames=1)
            continue

        # -- PYTHON --------------------------------------------------------------
        if isinstance(block, PythonStmt):
            try:
                exec(block.code, globals_ns)     # noqa: S102 exec is intended
                # console.print("[green]Python block executed successfully.[/]") # Optional success message
            except Exception as py_exec_e: # Catch any exec error
                console.print("[bold red]>>> Python Execution Error:[/]")
                console.print(f"[red]{type(py_exec_e).__name__}: {py_exec_e}[/]")
                console.print("[bold red]>>> Traceback:[/]")
                console.print_exception(max_frames=10) # Increase max_frames
            finally:
                # Always push changes after Python execution attempt
                try:
                    tables.push_all()
                except sqlite3.Error as e:
                     console.print(f"[red]DB sync error after Python: {e}[/]")
            continue

        # -- SQL -----------------------------------------------------------------
        if isinstance(block, SqlBlock):
            df_result = None
            try:
                # Try reading as a query first (SELECT, PRAGMA)
                df_result = pd.read_sql_query(block.sql, conn)
                globals_ns["_"] = df_result # Store last result
            except (pd.io.sql.DatabaseError, sqlite3.OperationalError) as e:
                # If read_sql fails, it might be DML/DDL or an error
                if "cannot operate on a closed database" in str(e).lower() or \
                   "no statement executed" in str(e).lower() :
                    # Likely DML/DDL, try executescript
                    try:
                        conn.executescript(block.sql)
                        conn.commit() # Commit changes for DML/DDL
                        console.print("[green]OK.[/]")
                    except sqlite3.Error as exec_e:
                         console.print(f"[red]SQL Error: {exec_e.__class__.__name__}: {exec_e}[/]")
                else:
                    # It was likely a genuine error in a SELECT-like query
                    console.print(f"[red]SQL Error: {e.__class__.__name__}: {e}[/]")
            except Exception as e: # Catch other potential pandas/SQL errors
                 console.print(f"[bold red]Unexpected SQL Error:[/]\n[red]{type(e).__name__}: {e}[/]")
            finally:
                 # Refresh Python view of tables if SQL might have changed them
                 try:
                     tables.refresh_all()
                     globals_ns.update(tables.tables) # Ensure globals reflect refreshed state
                     psession.completer = _build_completer(tables) # Update completer
                 except sqlite3.Error as e:
                      console.print(f"[red]DB sync error after SQL: {e}[/]")

            # Render result *after* refresh_all, only if read_sql succeeded
            if df_result is not None:
                _render_df(df_result)

            continue 