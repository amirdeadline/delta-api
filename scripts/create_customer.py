import requests
import argparse
import json
from termcolor import colored
import random
import string

# Setup command line arguments
parser = argparse.ArgumentParser(description="Create or delete objects in Delta SASE system.")
parser.add_argument("-c", "--customer", help="Customer name")
parser.add_argument("-d", "--delete", action="store_true", help="Delete the specified tenant and customer")
parser.add_argument("-n", "--num_customers", type=int, help="Number of customers to create")
args = parser.parse_args()

# API endpoint
API_ENDPOINT = "http://10.1.1.21:8053/api/v1/manage/"

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

def delete_request(path):
    """Function to send DELETE request."""
    full_url = f"{API_ENDPOINT}{path}/"
    try:
        response = requests.delete(full_url, headers=headers)
        response.raise_for_status()
        print(f"Deleted: {full_url}")
        successful_calls.append(full_url)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        failed_calls.append(full_url)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        failed_calls.append(full_url)

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
        successful_calls.append(full_url)
        return response_json
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        failed_calls.append(full_url)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        failed_calls.append(full_url)
        return None
    except ValueError:
        print("Invalid JSON response.")
        failed_calls.append(full_url)
        return None

def check_and_delete_existing(name, entity):
    """Function to check if a specific tenant or customer exists and delete if found."""
    # Construct the API endpoint based on the entity
    if entity == 'tenants':
        path = f"{entity}/?name={name}"
    elif entity == 'customers':
        path = f"{entity}/?name={name}&is_active=True"
    else:
        print("Invalid entity type.")
        return
    
    # Send GET request to check if the entity exists
    response = get_request(path)
    if response:
        if len(response) > 1:
            print(f"Multiple {entity} found with the name '{name}'. Cannot determine which one to delete.")
        else:
            item = response[0]
            item_id = item.get('id')
            item_name = item.get('name')
            print(f"{entity.capitalize()} '{item_name}' with ID '{item_id}' found. Deleting...")
            delete_request(f"{entity}/{item_id}")
    else:
        print(colored(f"No {entity} found with name '{name}'.", "yellow"))

def generate_random_string(length):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def delete_customer_and_contacts(customer_id):
    """Delete customer and its contacts."""
    # Delete contacts first
    contacts = get_request(f"contacts/?customer={customer_id}")
    if contacts:
        for contact in contacts:
            delete_request(f"contacts/{contact['id']}")
    
    # Delete customer
    delete_request(f"customers/{customer_id}")


if args.delete:
    customers = get_request("customers")
    if customers:
        for customer in customers:
            delete_customer_and_contacts(customer['id'])
    else:
        print("No customers found to delete.")
else:
    if args.num_customers:
        for i in range(1, args.num_customers + 1):
            customer_name = args.customer + str(i) if args.customer else generate_random_string(8)
            customer_data = {"name": customer_name}
            customer = post_request("customers", customer_data)
            if customer:
                print(f"Customer {i} created with ID:", customer.get("id"))
                # Create contacts for the customer
                contact_data = [
                    {"name": f"Contact {i}", "customer": customer["id"], "role": "Primary Contact", "email": f"contact{i}@example.com"}
                ]
                for contact in contact_data:
                    response = post_request("contacts", contact)
                    if response is None:
                        print("Failed to create contact:", contact['name'])
    else:
        customer_name = args.customer if args.customer else generate_random_string(8)
        customer_data = {"name": customer_name}
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

# Print successful and failed API calls
print("Successful API calls:")
for call in successful_calls:
    print(colored(call, "green"))
print("\nFailed API calls:")
for call in failed_calls:
    print(colored(call, "red"))
