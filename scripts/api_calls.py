import requests
import psycopg2
from psycopg2 import sql
import subprocess
import os
import time 
# n=30
# for i in range(n):
#     print("{:02d}".format(n-i), end='\r', flush=True)
#     time.sleep(1)
import threading

def get_input(input_list, user_has_responded):
    input("Press ENTER to continue...")
    user_has_responded.append(True)  # Flag that the user has responded

def countdown(n, user_has_responded):
    for i in range(n, 0, -1):
        if user_has_responded:
            break
        print(f"{i} seconds remaining...", end='\r', flush=True)
        time.sleep(1)

user_has_responded = []
input_thread = threading.Thread(target=get_input, args=([], user_has_responded))
countdown_thread = threading.Thread(target=countdown, args=(30, user_has_responded))

input_thread.start()
countdown_thread.start()

input_thread.join(timeout=30)
countdown_thread.join()

if input_thread.is_alive():
    print("Continuing after waiting for 30 seconds.")
else:
    print("User pressed ENTER.")





current_dir = os.path.dirname(os.path.abspath(__file__))
sql_file_path = os.path.join(current_dir, "queries.sql")

# Set the base url
base_url = 'http://192.168.172.71:8053'  # Replace with your base URL

# Function to post a new customer
def post_customer(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Customer creation successful")
        return response.json()
    else:
        print("Error in customer creation")
        return response.json()

# Function to post a new tenant
def post_tenant(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Tenant creation successful")
        return response.json()
    else:
        print("Error in tenant creation")
        return response.json()


def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to post a new site
def post_call(url, data):
    response = requests.post(url, json=data)
    if response.status_code < 220:
        print("Object creation successful", response.json())
        return response.json()
    else:
        print("Error in object creation", response.json())
        return None

def execute_query(query):
    db_conn_str = "dbname='delta98' user='admin' host='192.168.172.71' password='admin' port='5433'"
    conn = None

    try:
        conn = psycopg2.connect(db_conn_str)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        print("Query executed successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing query", error)
    finally:
        if conn is not None:
            conn.close()


# # Customer data
customer_data = {"name": "Jane Smith1",
                 "email": "jane.smith1@example.com",
                 "contact_number": "0987654321",
                 "company_name": "Smith Industries",
                 "company_address": "456 Maple Ave, Anytown, USA",
                 "is_active": True}
                 

# Create customer
customer_dict = post_customer(f'{base_url}/manage/customers/', customer_data)
customer_id = customer_dict.get('id', None) if customer_dict else None

# Tenant data
tenant_data = {
    "name": "Customer 1",
    "description": "Customer 1",
    "customer_id": customer_id,
    "enabled": True,
    "production": True
}


# Create tenant
tenant_dict = post_tenant(f'{base_url}/manage/tenants/', tenant_data)
print(tenant_dict)
tenant_id = tenant_dict.get('tenant_id', None) if tenant_dict else None

    
sql_commands = read_sql_file(sql_file_path)
# print(sql_commands)
execute_query(sql_commands)


    
site_group_data = {
    "name": "Site Group 1",
    "tags": [{"name":"sitetesttag1", "value":{}}, {"name":"testtag2"}],
    "type": "hub-spoke",
    "description": "string"
}
site_group_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/sitegroups/', site_group_data)
# tenant_id="1001"
# Site data
site_data = {
    "name": "Site 1",
    "tags": [{"name":"sitetesttag1", "value":{}}, {"name":"testtag2"}],
    "type": "hub",
    "description": "string",
    "site_group": ["Site Group 1"]
}
# Site data
site2_data = {
    "name": "Site 2",
    "tags": [{"name":"sitetesttag1", "value":{}}, {"name":"testtag2"}],
    "type": "branch",
    "description": "string",
    "site_group": ["Site Group 1"]
}
# Create site
site_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/sites/', site_data)
site2_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/sites/', site2_data)

# Site data
device_data = {
    "serial_number": "111111",
    "model": 1,
    "software": 1,
    "site": 1
}
# Site data
device2_data = {
    "serial_number": "22222",
    "model": 1,
    "software": 1,
}
# Create site
device_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/devices/', device_data)
device2_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/devices/', device2_data)


eth_data= {
  "name": "eth0",
  "mtu": 1500,
  "adjust_mss": 1460,
  "dhcp_client": False,
  "role": "lan",
  "type": "eth",
  "vrf": "200",
  "admin_state": True
}
eth_dict={}
for e in range(10):
    eth_data["name"]= "eth"+str(e) 
    eth_dict[e]=post_call(f'{base_url}/tenant/{tenant_id}/network/devices/{device_dict["id"]}/interfaces/', eth_data)
    print(f"interface eth{e} created \n")

bond_data= {
  "name": "bond2",
  "mtu": 1500,
  "adjust_mss": 1460,
  "dhcp_client": False,
  "role": "lan",
  "type": "bond",
  "vrf": "100",
  "admin_state": True,
  "hash": "layer2+3",
  "members": ["eth1", "eth2"]
}

bond_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/devices/{device_dict["id"]}/interfaces/', bond_data)

bridge_data= {
  "name": "bridge1",
  "mtu": 1500,
  "adjust_mss": 1460,
  "dhcp_client": False,
  "role": "lan",
  "type": "bridge",
  "vrf": "100",
  "admin_state": True,
  "members":["eth3"]
}


bridge_dict = post_call(f'{base_url}/tenant/{tenant_id}/network/devices/{device_dict["id"]}/interfaces/', bridge_data)