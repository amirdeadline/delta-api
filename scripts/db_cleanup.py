import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import subprocess


# Connection parameters
host = '127.0.0.1'
port = '5432'
user = 'admin'
password = 'admin'

# Name of the database to delete and recreate
db_name = 'postgres'

# Create a connection to the PostgreSQL server
conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password
)

# Set the connection to autocommit mode to execute the 'CREATE DATABASE' command
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Create a cursor object
cur = conn.cursor()

try:
    # Disconnect all active connections to the database
    cur.execute(f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{db_name}'
          AND pid <> pg_backend_pid();
    """)
    print(f"All active connections to database {db_name} have been disconnected.")
except psycopg2.Error as e:
    print(f"An error occurred while disconnecting active connections to database {db_name}: {e}")

try:
    # Delete the database
    cur.execute(f'DROP DATABASE IF EXISTS {db_name};')
    print(f"Database {db_name} deleted successfully.")
except psycopg2.Error as e:
    print(f"An error occurred while deleting database {db_name}: {e}")

try:
    # Recreate the database
    cur.execute(f'CREATE DATABASE {db_name};')
    print(f"Database {db_name} recreated successfully.")

    # After recreating the database, run the shell commands
    commands = [
        'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete',
        'find . -path "*/migrations/*.pyc" -delete',
        'echo y | pip uninstall django',
        'pip install django',
        'python3 /root/delta_api/delta_sase/manage.py makemigrations',
        'python3 /root/delta_api/delta_sase/manage.py migrate',
        'python3 /root/delta_api/delta_sase/manage.py create_public',
        'python3 /root/delta_api/delta_sase/manage.py create_reserve',
        'python3 /root/delta_api/delta_sase/manage.py runserver 0.0.0.0:8053',
    ]
    for command in commands:
        subprocess.call(command, shell=True)
except psycopg2.Error as e:
    print(f"An error occurred while creating database {db_name}: {e}")

# Close the cursor and the connection
cur.close()
conn.close()