import requests
import argparse
import json

# Setup command line arguments
parser = argparse.ArgumentParser(description="Create or delete objects in Delta SASE system.")
parser.add_argument("-c", "--customer", required=True, help="Customer name")
parser.add_argument("-t", "--tenant", required=True, help="Tenant name")
parser.add_argument("-d", "--delete", action="store_true", help="Delete the specified tenant and customer")
args = parser.parse_args()

# API endpoint
API_ENDPOINT = "http://10.1.1.21:8053/api/v1/manage/"

# Common headers
headers = {'user_id': 'amir@deltasase.com'}

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

def delete_request(path):
    """Function to send DELETE request."""
    full_url = f"{API_ENDPOINT}{path}/"
    try:
        response = requests.delete(full_url, headers=headers)
        response.raise_for_status()
        print(f"Deleted: {full_url}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

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
        return response_json
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except ValueError:
        print("Invalid JSON response.")
        return None

if args.delete:
    # Execute deletion of tenant and customer
    check_and_delete_existing(args.tenant, 'tenants')
    check_and_delete_existing(args.customer, 'customers')
else:
    # Create customer and tenant
    customer_data = {"name": args.customer}
    customer = post_request("customers", customer_data)
    if customer:
        print("Customer created with ID:", customer.get("id"))
        # Create contacts for the customer
        contact_data = [
            {"name": "John Doe", "customer": customer["id"], "role": "Primary Contact", "email": "john.doe@example.com"},
            {"name": "Jane Doe", "customer": customer["id"], "role": "Secondary Contact", "email": "jane.doe@example.com"}
        ]
        for contact in contact_data:
            response = post_request("contacts", contact)
            if response is None:
                print("Failed to create contact:", contact['name'])

        # Create tenant
        tenant_data = {
            "name": args.tenant,
            "customer": customer["id"],
            "tags": []
        }
        tenant = post_request("tenants", tenant_data)
        if tenant:
            print("Tenant created with ID:", tenant.get("id"))
