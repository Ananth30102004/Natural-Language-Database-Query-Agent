from pathlib import Path
import sqlite3
from mcp.server.fastmcp import FastMCP
# from sqlalchemy import table

mcp = FastMCP("DataPilot")

DB_Path = Path(__file__).parent / "erp_db.db"

def connect():
       """Connect to SQLite in read-only mode."""
       conn = sqlite3.connect(
              f"{DB_Path.resolve().as_uri()}?mode=ro",
              uri=True
       )
       conn.row_factory = sqlite3.Row
       return conn

@mcp.tool()
def list_tables() -> list[str]:
       """List all tables from the SQLite database"""
       with connect() as conn:
              rows = conn.execute(  """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """).fetchall()
              return [row["name"] for row in rows]
       

@mcp.tool()
def describe_table(table:str) -> dict:
    """Describe the columns of a table in the SQLite database"""
    if table not in list_tables():
              return {"error": f"Table {table} does not exist in the database"}

    with connect() as conn:
        columns = conn.execute(f"PRAGMA table_info({table})").fetchall()

        count = conn.execute(f"SELECT COUNT(*) as count FROM {table}").fetchone()[0]

    return {
            "table": table,
            "row_count": count,
            "columns":[dict(col)for col in columns]
       }

def validate_sql(query: str) -> bool:
    query = query.strip()

    if not query:
        return False

    # Only allow SELECT queries
    if not query.upper().startswith("SELECT"):
        return False

    # Reject multiple SQL statements
    if ";" in query.rstrip(";"):
        return False

    return True


@mcp.tool()
def execute_sql(query : str ,limit:int = 5) ->list[dict] | str:
    """Execute a SQL query on the SQLite database and return the results"""

    query = query.strip()

    # Step 1: Validate SQL
    if not validate_sql(query):
        return "Error: Only a single SELECT query is allowed."

    limit = max(1, min(limit, 100))

    try:   
        with connect() as conn:
            conn.execute("PRAGMA query_only = ON")
            rows = conn.execute(query).fetchmany(limit)

        return [dict(row) for row in rows] if rows else "No results found"
    
    except sqlite3.OperationalError as e:
        return f"SQL Execution Error: {e}"

    except sqlite3.Error as e:
        return f"Database Error: {e}"

if __name__ == "__main__":
      mcp.run()

