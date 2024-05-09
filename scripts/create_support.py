import requests
import argparse
import json

# API endpoint
API_ENDPOINT = "http://10.1.1.21:8053/api/v1/"

# Common headers
headers = {'user_id': 'amir@deltasase.com'}

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
# Create regions
regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "sa-east-1"]
for region in regions:
    region_data = {"name": region, "cloud": "aws"}
    post_request("network/regions", region_data)

# Create products and categories
products = ["SDWAN", "Security", "CASB", "SASE", "Ingress"]
for product in products:
    product_data = {"name": product, "unit":"qt", "price":1000}
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
routing_protocols = ["BGP", "Static", "OSPF", "ISIS"]
for protocol in routing_protocols:
    protocol_data = {"name": protocol}
    post_request("support/protocols/routing", protocol_data)

# Interface Roles
interface_roles = ["LAN", "Internet", "WAN", "HA", "MGMT", "Lo0", "Overlay",
                   "Bridge", "SVI", "LAG", "Eth", "VLAN", "Loopback", "Tunnel", "VTI", "Veth"]
for role in interface_roles:
    role_data = {"name": role}
    post_request("support/interfaces/roles", role_data)

# Device Models
device_models = ["DSN-1000", "DSN-3000", "DSN-2000"]
for model in device_models:
    model_data = {"name": model}
    post_request("support/devices/models", model_data)

# VRF Roles
vrf_roles = ["LAN", "Internet", "WAN", "Overlay", "MGMT", "CTRL", "SASE"]
for vrf_role in vrf_roles:
    vrf_role_data = {"name": vrf_role}
    post_request("support/vrf/role", vrf_role_data)

# LACP Hash Options
lacp_hash_options = ["src-l2", "src-dst-l2", "src-l3", "src-dst-l3", "src-l4", "src-dst-l4"]
for option in lacp_hash_options:
    option_data = {"name": option}
    post_request("support/lacp/hash", option_data)


print("All configurations and objects created successfully.")