# default_settings.py
from django.db import connection

def get_table_names():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'default'""")
        return [row[0] for row in cursor.fetchall()]

def copy_data_from_default(tenant):
    table_names = get_table_names()
    with connection.cursor() as cursor:
        for table in table_names:
            cursor.execute(f"""
                INSERT INTO {tenant.schema_name}.{table} 
                SELECT * FROM default.{table}
            """)
