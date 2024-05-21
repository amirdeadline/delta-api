import psycopg2

def execute_query(ip, port, username, password, db_name, schema_name, query):
    conn = None
    try:
        # Establish connection to PostgreSQL database
        conn = psycopg2.connect(
            host=ip,
            port=port,
            user=username,
            password=password,
            dbname=db_name
        )

        # Create a cursor object
        cur = conn.cursor()

        # Set the schema 
        cur.execute(f"SET search_path TO {schema_name}")

        # Execute the SQL query
        cur.execute(query)

        # Fetch all the records
        rows = cur.fetchall()

        for row in rows:
            print(row)

        # Close the communication with the PostgreSQL database server
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

# # Test the function
# execute_query('192.168.172.71', 5433, 'admin', 'admin', 'delta98', 'Tenant_1001',
#  "SELECT * FROM information_schema.tables WHERE table_schema = 'Tenant_1001' AND table_name = 'interfaces_app_interfacetype';")

execute_query('10.1.1.21', 5432, 'admin', 'admin', 'postgress', 'Tenant_1001',
 'select * from "Tenant_1001"."interfaces_app_interfacetype"')
