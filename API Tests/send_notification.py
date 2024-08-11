import requests
import variabels
from requests.auth import HTTPBasicAuth

# Konfiguration
hostname = variabels.hostname
username = variabels.username
password = variabels.password

notification_url = f'http://{hostname}/fhapi/v1/api/rest/notification'

notification_payload = {
    "formatVersion": 1,
    "topicId": "org.example.test",
    "timeoutMinutes": 1,
    "displayHints": ["styleInfo"],
    "retention": 1,
    "terminals": ["push-notification"],
    "content": {
        "utf8": {
            "de": {
                "title": "Test Nachricht",
                "body": "Test"
            },
            "en": {
                "title": "Test message",
                "body": "Test"
            }
        }
    }
}

try:
    response = requests.post(
        notification_url,
        json=notification_payload,
        auth=HTTPBasicAuth(username, password),
        verify=False
    )

    response.raise_for_status()

    print("Notification posted successfully!")
    print("Response:", response.json())

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Text:", response.text)
