import requests
import json
from termcolor import colored  # Added for colorizing output
import subprocess

# API endpoint
API_ENDPOINT = "http://10.1.1.21:8053/"


def run_generate_jwt_script():
    """Function to run the generate_jwt.py script."""
    command = "python3 /root/delta_api/JWT/generate_jwt.py"
    try:
        subprocess.run(command, shell=True, check=True)
        print("generate_jwt.py script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def load_jwt_token(file_path):
    """Load JWT token from a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

run_generate_jwt_script()   
jwt_token = load_jwt_token("/root/delta_api/JWT/amir_jwt.txt")

# Common headers
headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

def post_request(path, data):
    """Function to send POST request and handle errors."""
    full_url = f"{API_ENDPOINT}{path}/"
    json_data = json.dumps(data, indent=4)
    
    # Print formatted JSON data
    ## print("Data being sent as JSON:", json_data)
    try:
        response = requests.post(full_url, json=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        # print("Response JSON:", json.dumps(response_json, indent=4))
        # Print success message in green color
        print(colored(f"Item {path} {data['name']} created!", "green"))
        return response_json
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        # Print failure message in red color
        print(colored(f"Item {path} {data['name']} failed to create", "red"))
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        # Print failure message in red color
        print(colored(f"Item {path} {data['name']} failed to create", "red"))
        return None
    except ValueError:
        print("Invalid JSON response.")
        # Print failure message in red color
        print(colored(f"Item {path} {data['name']} failed to create", "red"))
        return None

# Create regions
regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "sa-east-1"]
for region in regions:
    region_data = {"name": region, "cloud": "aws"}
    post_request("network/regions", region_data)

# Create products and categories
products = ["SDWAN", "Security", "CASB", "SASE", "Ingress"]
for product in products:
    product_data = {"name": product, "unit": "qt", "price": 1000}
    post_request("manage/products", product_data)

# IKE and ESP configurations
ike_encryptions = ["AES-128", "AES-256", "3DES"]
ike_hashes = ["SHA1", "SHA256", "MD5"]
ike_dh_groups = ["Group1", "Group2", "Group5"]
ike_rpfs = ["YES", "NO"]
esp_encryptions = ["AES-128", "AES-256", "3DES"]
esp_hashes = ["SHA1", "SHA256", "MD5"]
esp_dh_groups = ["Group1", "Group2", "Group5"]
esp_pfss = ["YES", "NO"]

# IKE and ESP configurations
for encryption in ike_encryptions:
    post_request("support/ike/encrypt", {"name": encryption})

for hash in ike_hashes:
    post_request("support/ike/hash", {"name": hash})

for dh_group in ike_dh_groups:
    post_request("support/ike/dh", {"name": dh_group})

for rpf in ike_rpfs:
    post_request("support/ike/rpf", {"name": rpf})

for encryption in esp_encryptions:
    post_request("support/esp/encrypt", {"name": encryption})

for hash in esp_hashes:
    post_request("support/esp/hash", {"name": hash})

for dh_group in esp_dh_groups:
    post_request("support/esp/dh", {"name": dh_group})

for pfs in esp_pfss:
    post_request("support/esp/pfs", {"name": pfs})

# Create Routing Protocols, Interface Roles, Device Models, VRF Roles, LACP Hash Options
routing_protocols = ["BGP", "Static", "OSPF", "ISIS"]
interface_roles = ["LAN", "Internet", "WAN", "HA", "MGMT", "Lo0", "Overlay",
                   "Bridge", "SVI", "LAG", "Eth", "VLAN", "Loopback", "Tunnel", "VTI", "Veth"]
device_models = ["DSN-1000", "DSN-3000", "DSN-2000"]
vrf_roles = ["LAN", "Internet", "WAN", "Overlay", "MGMT", "CTRL", "SASE"]
lacp_hash_options = ["src-l2", "src-dst-l2", "src-l3", "src-dst-l3", "src-l4", "src-dst-l4"]

# Routing Protocols
for protocol in routing_protocols:
    protocol_data = {"name": protocol}
    post_request("support/protocols/routing", protocol_data)

# Interface Roles
for role in interface_roles:
    role_data = {"name": role}
    post_request("support/interfaces/roles", role_data)

# Device Models
for model in device_models:
    model_data = {"name": model}
    post_request("support/devices/models", model_data)

# VRF Roles
for vrf_role in vrf_roles:
    vrf_role_data = {"name": vrf_role}
    post_request("support/vrf/role", vrf_role_data)

# LACP Hash Options
for option in lacp_hash_options:
    option_data = {"name": option}
    post_request("support/lacp/hash", option_data)

print("All configurations and objects created successfully.")
