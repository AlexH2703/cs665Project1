import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

def get_db_connection():
    """
    Establish and return a connection to the database.
    """
    conn = None
    try:
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
    except Exception as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_query(query, params=None):
    """
    Executes SQL and returns results if the query returns any (e.g. SELECT).
    Automatically commits changes for data-modifying queries.
    """
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Only try to fetch results if the query returned any (SELECT or similar)
            if cursor.description is not None:
                return cursor.fetchall()
            else:
                conn.commit()
                return None
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()