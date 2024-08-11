import requests
from requests.auth import HTTPBasicAuth
import variabels

# Configuration from variabels.py
hostname = variabels.hostname
sysap_uuid = variabels.sysap_uuid
username = variabels.username
password = variabels.password

divice_id = input("Enter device id: ")

# URL to get information about a specific device
devices_url = f'http://{hostname}/fhapi/v1/api/rest/device/{sysap_uuid}/{device_id}'

try:
    # Send request
    response = requests.get(devices_url, auth=HTTPBasicAuth(username, password), verify=False)
    # Check if the request was successful
    response.raise_for_status()

# Handle errors
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
