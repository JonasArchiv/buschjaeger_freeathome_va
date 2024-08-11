import requests
from requests.auth import HTTPBasicAuth
import variabels

# Configuration from variabels.py
hostname = variabels.hostname
username = variabels.username
password = variabels.password

# URL to get all devices
devices_url = f'http://{hostname}/fhapi/v1/api/rest/devicelist'

try:
    # Send request to get all devices
    response = requests.get(devices_url, auth=HTTPBasicAuth(username, password), verify=False)
    # Check if the request was successful
    response.raise_for_status()

    # Get the list of all devices
    devices = response.json()

    # Print the list of all device IDs
    print("List of all device IDs:")
    for sysap, device_list in devices.items():
        for device_id in device_list:
            print(device_id)

# Handle errors
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
