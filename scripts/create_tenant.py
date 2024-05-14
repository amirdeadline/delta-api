import requests
import argparse
import json
import random
from termcolor import colored

# Setup command line arguments
parser = argparse.ArgumentParser(description="Create or delete objects in Delta SASE system.")
parser.add_argument("-n", "--number", type=int, help="Number of tenants to create")
parser.add_argument("-t", "--tenant", help="Specify a single tenant to create")
parser.add_argument("-d", "--delete", help="Delete a specific tenant by name or delete all tenants with IDs greater than the specified value")
args = parser.parse_args()

# API endpoint
API_ENDPOINT = "http://10.1.1.21:8053/manage/"

def load_jwt_token(file_path):
    """Load JWT token from a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

jwt_token = load_jwt_token("/root/delta_api/JWT/amir_jwt.txt")

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
}

# Tracking successful and failed API calls
successful_calls = []
failed_calls = []

def get_request(path):
    """Function to send GET request and return the response as JSON."""
    full_url = f"{API_ENDPOINT}{path}/"
    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return []

def patch_request(path, data):
    """Function to send PATCH request and handle errors."""
    full_url = f"{API_ENDPOINT}{path}/"
    json_data = json.dumps(data, indent=4)
    print("Data being sent as JSON:", json_data)  # Print formatted JSON data
    try:
        response = requests.patch(full_url, json=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        print("Response JSON:", json.dumps(response_json, indent=4))
        successful_calls.append("PATCH "+full_url)
        return response_json
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        failed_calls.append("PATCH "+full_url)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        failed_calls.append("PATCH "+full_url)
        return None
    except ValueError:
        print("Invalid JSON response.")
        failed_calls.append("PATCH "+full_url)
        return None
    
def delete_request(path):
    """Function to send DELETE request."""
    full_url = f"{API_ENDPOINT}{path}/"
    try:
        response = requests.delete(full_url, headers=headers)
        response.raise_for_status()
        print(f"Deleted: {full_url}")
        successful_calls.append("DELETE "+full_url)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        failed_calls.append("DELETE "+full_url)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        failed_calls.append("DELETE "+full_url)

def post_request(path, data):
    """Function to send POST request and handle errors."""
    full_url = f"{API_ENDPOINT}{path}/"
    json_data = json.dumps(data, indent=4)
    print("Data being sent as JSON:", json_data)  # Print formatted JSON data
    try:
        response = requests.post(full_url, json=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        print("Response JSON:", json.dumps(response_json, indent=4))
        successful_calls.append("POST "+full_url)
        return response_json
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        failed_calls.append("POST "+full_url)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        failed_calls.append("POST "+full_url)
        return None
    except ValueError:
        print("Invalid JSON response.")
        failed_calls.append("POST "+full_url)
        return None

def create_tenant(name, customer_id):
    """Function to create a tenant."""
    tenant_data = {
        "name": name,
        "customer": customer_id,
        "tags": [
            {"key": "Environment", "value": "Test"},
            {"key": "Priority", "value": "High"}
        ]
    }
    tenant = post_request("tenants", tenant_data)
    if tenant:
        print("Tenant created with ID:", tenant.get("id"))

# Handle tenant creation
if args.number:
    customers = get_request("customers")
    if not customers:
        print("No customers found. Please create customers first.")
    else:
        for _ in range(args.number):
            random_customer = random.choice(customers)
            create_tenant(f"Tenant_{random.randint(1, 100)}", random_customer["id"])
elif args.tenant:
    customers = get_request("customers")
    if not customers:
        print("No customers found. Please create customers first.")
    else:
        random_customer = random.choice(customers)
        create_tenant(args.tenant, random_customer["id"])
else:
    customers = get_request("customers")
    if not customers:
        print("No customers found. Please create customers first.")
    else:
        random_customer = random.choice(customers)
        create_tenant(f"Tenant_{random.randint(1, 100)}", random_customer["id"])

# Handle tenant deletion
if args.delete:
    if args.delete == '0':
        # Delete all tenants with IDs greater than 2
        tenants = get_request("tenants")
        if tenants:
            for tenant in tenants:
                if tenant["id"] > 2:
                    patch_request(f"tenants/{tenant['id']}", {"enabled": False})
                    delete_request(f"tenants/{tenant['id']}")
    else:
        # Delete a specific tenant by name
        tenants = get_request(f"tenants/?name={args.delete}")
        if tenants:
            for tenant in tenants:
                patch_request(f"tenants/{tenant['id']}", {"enabled": False})
                delete_request(f"tenants/{tenant['id']}")

# Print successful and failed API calls
print("Successful API calls:")
for call in successful_calls:
    print(colored(call, "green"))
print("\nFailed API calls:")
for call in failed_calls:
    print(colored(call, "red"))
