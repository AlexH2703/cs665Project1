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
        print("Connection successful!")
    except Exception as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_query(query, params=None):
    """
    Execute a query and return the result.
    :param query: The SQL query to execute.
    :param params: Any parameters for the query (default is None).
    :return: The result of the query.
    """
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()
