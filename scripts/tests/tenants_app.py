import requests

# Configuration
base_url = 'http://10.1.1.21:8053/api/v1/'  # Adjust this to your actual API endpoint
headers = {'Content-Type': 'application/json', 'user_id': 'test@deltasase.com'}  # Include your actual user_id or authentication token

# Helper function to send requests
def send_request(method, url, data=None):
    try:
        response = requests.request(method, url, json=data, headers=headers)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        if response.text:
            return response.json()  # Return JSON if there is a response body
        return {}
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err} - {response.text}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Create, update, and delete resources
def manage_resources():
    try:
        # Create Customer
        customer_data = {"name": "Customer A", "company_name": "Company A"}
        customer = send_request('POST', f'{base_url}manage/customers/', customer_data)
        customer_id = customer.get('id')

        # Create Contact for Customer
        contact_data = {"customer": customer_id, "name": "Contact A", "email": "contact@example.com"}
        contact = send_request('POST', f'{base_url}manage/contacts/', contact_data)
        contact_id = contact.get('id')

        # Create Tenant for Customer
        tenant_data = {"customer": customer_id, "name": "Tenant A", "schema_name": "tenant_a"}
        tenant = send_request('POST', f'{base_url}manage/tenants/', tenant_data)
        tenant_id = tenant.get('id')

        # Create SDWAN Software
        sdwan_data = {"name": "SDWAN Product A", "url": "http://sdwan-product-a.com"}
        sdwan_product = send_request('POST', f'{base_url}support/sdwan/software/', sdwan_data)
        sdwan_product_id = sdwan_product.get('id')

        # Create License
        license_data = {"name": "License A","unit": "qt",  "price": 100.00}
        license = send_request('POST', f'{base_url}manage/licenses/', license_data)
        license_id = license.get('id')

        # Update Customer
        updated_customer_data = {"company_name": "Updated Company A"}
        send_request('PATCH', f'{base_url}manage/customers/{customer_id}/', updated_customer_data)

        # Update Tenant to include products and licenses
        updated_tenant_data = {"products": [sdwan_product_id], "licenses": [license_id]}
        send_request('PUT', f'{base_url}manage/tenants/{tenant_id}/', updated_tenant_data)

        # Cleanup resources in reverse order of creation
        send_request('DELETE', f'{base_url}manage/tenants/{tenant_id}/')
        send_request('DELETE', f'{base_url}manage/licenses/{license_id}/')
        send_request('DELETE', f'{base_url}support/sdwan/software/{sdwan_product_id}/')
        send_request('DELETE', f'{base_url}manage/contacts/{contact_id}/')
        send_request('DELETE', f'{base_url}manage/customers/{customer_id}/')

        print("All operations completed successfully.")

    except Exception as e:
        print(f'Failed to manage resources due to: {e}')

# Execute the resource management function
manage_resources()
