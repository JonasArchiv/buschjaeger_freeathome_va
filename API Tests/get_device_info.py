import requests
from requests.auth import HTTPBasicAuth
import variabels

# Configuration from variabels.py
hostname = variabels.hostname
sysap_uuid = variabels.sysap_uuid
username = variabels.username
password = variabels.password

device_id = input("Enter device id: ")

# URL to get information about a specific device
devices_url = f'http://{hostname}/fhapi/v1/api/rest/device/{sysap_uuid}/{device_id}'

try:
    # Send request
    response = requests.get(devices_url, auth=HTTPBasicAuth(username, password), verify=False)
    # Check if the request was successful
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Extract and display the information
    device_info = data.get(sysap_uuid, {}).get('devices', {}).get(device_id, {})

    if not device_info:
        print(f"No information found for device id: {device_id}")
    else:
        print(f"Device ID: {device_id}")
        print(f"Display Name: {device_info.get('displayName', 'N/A')}")
        print(f"Native ID: {device_info.get('nativeId', 'N/A')}")
        print(f"Unresponsive: {device_info.get('unresponsive', 'N/A')}")

        channels = device_info.get('channels', {})
        for channel_id, channel_info in channels.items():
            print(f"\nChannel ID: {channel_id}")
            print(f"  Display Name: {channel_info.get('displayName', 'N/A')}")
            print(f"  Function ID: {channel_info.get('functionID', 'N/A')}")

            inputs = channel_info.get('inputs', {})
            print("  Inputs:")
            for input_id, input_info in inputs.items():
                print(f"    Input ID: {input_id}")
                print(f"      Pairing ID: {input_info.get('pairingID', 'N/A')}")
                print(f"      Value: {input_info.get('value', 'N/A')}")

            outputs = channel_info.get('outputs', {})
            print("  Outputs:")
            for output_id, output_info in outputs.items():
                print(f"    Output ID: {output_id}")
                print(f"      Pairing ID: {output_info.get('pairingID', 'N/A')}")
                print(f"      Value: {output_info.get('value', 'N/A')}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
