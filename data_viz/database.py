import sqlite3


class Database:
  """
  A class for interacting with a SQLite database.
  """

  @staticmethod
  def connect(db_path):
    """
    Connects to the provided database path.

    Args:
      db_path: The path to the SQLite database file.

    Returns:
      A connection object to the database or None on error.
    """
    try:
      conn = sqlite3.connect(db_path)
      return conn
    except sqlite3.Error as e:
      print("Error connecting to database:", e)
      return None
   
  @staticmethod
  def execute_query(conn, query, params=()):
    """
    Executes a query on the provided connection.

    Args:
      conn: The connection object to the database.
      query: The SQL query to execute.
      params: A tuple of parameters for the query (optional).

    Returns:
      A cursor object containing the results or None on error.
    """
    try:
      cursor = conn.cursor()
      cursor.execute(query, params)
      return cursor
    except sqlite3.Error as e:
      print("Error executing query:", e)
      return None

  @staticmethod
  def fetch_all(cursor):
    """
    Fetches all rows from the provided cursor.

    Args:
      cursor: The cursor object containing the query results.

    Returns:
      A list of tuples representing the fetched rows or None on error.
    """
    if cursor:
      try:
        return cursor.fetchall()
      except sqlite3.Error as e:
        print("Error fetching data:", e)
        return None
    else:
      print("Invalid cursor object.")
      return None

  @staticmethod
  def fetch_one(cursor):
    """
    Fetches a single row from the provided cursor.

    Args:
      cursor: The cursor object containing the query results.

    Returns:
      A tuple representing the fetched row or None on error/no data.
    """
    if cursor:
      try:
        return cursor.fetchone()
      except sqlite3.Error as e:
        print("Error fetching data:", e)
        return None
    else:
      print("Invalid cursor object.")
      return None

  @staticmethod
  def get_table_names(conn):
    """
    Retrieves all table names from the database.

    Args:
      conn: The connection object to the database.

    Returns:
      A list of table names or None on error.
    """
    cursor = Database.execute_query(conn, "SELECT * FROM sqlite_master WHERE type='table';")
    if cursor:
      return [row[0] for row in Database.fetch_all(cursor)]
    else:
      return None
    
  @staticmethod
  def fetch_all_columns(conn, table):
    """
    Fetches all columns from the provided table.

    Args:
      table: The name of the table to fetch columns from.

    Returns:
      A list of tuples representing the columns or None on error.
    """
    query = f"SELECT * FROM {table}"
    cursor = Database.execute_query(conn, query)
    return Database.fetch_all(cursor)
    
  @staticmethod
  def cursor_to_df(cursor):
      """
      Converts a cursor object to a pandas DataFrame.

      Args:
        cursor: The cursor object containing the query results.

      Returns:
        A pandas DataFrame representing the query results or None on error.
      """
      import pandas as pd
      if cursor:
          try:
              # Fetch all rows from the cursor
              rows = cursor.fetchall()
              # Check if any rows were fetched
              if len(rows) > 0:
                  # Get column names from cursor description
                  columns = [description[0] for description in cursor.description]
                  # Create DataFrame from rows and columns
                  df = pd.DataFrame(rows, columns=columns)
                  return df
              else:
                  print("Cursor has no data.")
                  return None
          except sqlite3.Error as e:
              print("Error converting cursor to DataFrame:", e)
              return None
      else:
          print("Invalid cursor object.")
          return None
    
