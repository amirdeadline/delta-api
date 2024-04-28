"""

interfaces_app_interfacerole
interfaces_app_interfacetype
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys


def execute_query(ip, port, username, password, db_name, query):
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
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error", error)
    finally:
        if conn is not None:
            conn.close()

def create_interface_types(ip, port, username, password, db_name):
    query = f"""
        INSERT INTO "{schema_name}"."interfaces_app_interfacetype" (type) 
        VALUES 
        ('ethernet'),
        ('bonding'),
        ('dummy'),
        ('bridge'),
        ('openvpn'),
        ('loopback'),
        ('tunnel'),
        ('virtual-ethernet'),
        ('vti'),
        ('vxlan'),
        ('wireless'),
        ('wireguard'),
        ('wwan'),
        ('sstpc');
    """
    execute_query(ip, port, username, password, db_name, query)


def create_interface_types(schema_name, ip, port, username, password, db_name):
    query = f"""
        INSERT INTO "{schema_name}"."interfaces_app_interfacetype" (type) 
        VALUES 
        ('ethernet'),
        ('bonding'),
        ('dummy'),
        ('bridge'),
        ('openvpn'),
        ('loopback'),
        ('tunnel'),
        ('virtual-ethernet'),
        ('vti'),
        ('vxlan'),
        ('wireless'),
        ('wireguard'),
        ('wwan'),
        ('sstpc');
    """
    execute_query(ip, port, username, password, db_name, query)


def create_interface_roles(schema_name, ip, port, username, password, db_name):
    query = f"""
        INSERT INTO "{schema_name}"."interfaces_app_interfacerole" (role) 
        VALUES 
        ('lan'),
        ('internet'),
        ('private_underlay'),
        ('v-internet'),
        ('v-ctrl'),
        ('mgmt'),
        ('sdwan'),
        ('sase'),
        ('ctrl');
        """
    execute_query(ip, port, username, password, db_name, query)


if __name__ == "__main__":
    # These variables should come from your application's configuration
    db_name = 'delta98'  # replace with your database name
    username = 'admin'  # replace with your username
    password = 'admin'  # replace with your password
    ip = '192.168.172.71'  # replace with your host
    port = '5433'  # replace with your port

    # schema_name will come as a command line argument
    if len(sys.argv) > 1:
        schema_name = sys.argv[1]
        # create_interface_types(schema_name, ip, port, username, password, db_name)
        # create_interface_roles(schema_name, ip, port, username, password, db_name)

        query = f"""
            INSERT INTO "{schema_name}"."interfaces_app_interfacetype" (type) 
            VALUES 
            ('ethernet'),
            ('bonding'),
            ('dummy'),
            ('bridge'),
            ('openvpn'),
            ('loopback'),
            ('tunnel'),
            ('virtual-ethernet'),
            ('vti'),
            ('vxlan'),
            ('wireless'),
            ('wireguard'),
            ('wwan'),
            ('sstpc');
        """
        execute_query(ip, port, username, password, db_name, query)
    else:
        print("Please provide a schema name as an argument when running the script.")
