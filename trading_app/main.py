# # Note: the module name is psycopg, not psycopg3
# import psycopg2
# from psycopg2.rows import dict_row
# from pathlib import Path
#
#
# # read sql query
# def read_sql_query(sql_path: Path) -> str:
#     """Reads a SQL file and returns the query as a string."""
#     return Path(sql_path).read_text()
#
#
# raw_sql = read_sql_query(Path("../sql/test.sql"))
# # # placeholder = {"id": 1}
#
#
# # Connect to an existing database
# with psycopg2.connect(
#     host="localhost",
#     dbname="postgres",
#     user="postgres",
#     password="password",
#     port="5432",
#     row_factory=dict_row,
# ) as conn:
#     # Open a cursor to perform database operations
#     with conn.cursor() as cur:
#         # Execute a command: this creates a new table
#         cur.execute(raw_sql)
#
#         # Pass data to fill a query placeholders and let Psycopg perform
#         # the correct conversion (no SQL injections!)
#         cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
#
#         # Query the database and obtain data as Python objects.
#         cur.execute("SELECT * FROM test")
#         cur.fetchone()
#         # will return (1, 100, "abc'def")
#
#         # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
#         # of several records, or even iterate on the cursor
#         for record in cur:
#             print(record)
#
#         # Make the changes to the database persistent
#         conn.commit()
