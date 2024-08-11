import requests
from requests.auth import HTTPBasicAuth
import variabels

# Konfigurationsvariablen aus variabels.py
hostname = variabels.hostname
sysap_uuid = variabels.sysap_uuid
username = variabels.username
password = variabels.password

device_url = f'http://{hostname}/fhapi/v1/api/rest/device/{{sysap_uuid}}/{{device_id}}'


def lampe_steuern(device_id, channel_id, status):
    full_url = device_url.format(sysap_uuid=sysap_uuid, device_id=device_id)

    output_value = "1" if status == "an" else "0"

    request_body = {
        "outputs": {
            f"odp{channel_id[-4:]}": {"value": output_value}
        }
    }

    try:
        response = requests.post(
            full_url,
            auth=HTTPBasicAuth(username, password),
            json=request_body,
            headers={'Content-Type': 'application/json'},
            verify=False
        )

        response.raise_for_status()

        print("Status erfolgreich geändert.")
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Ändern des Status: {e}")


def main():
    print("Willkommen zum Lampe Steuerungstool!")

    while True:
        device_id = input("Bitte gib die Geräte-ID der Lampe ein: ").strip()
        if not device_id:
            print("Gültige Geräte-ID eingeben. Versuche es bitte erneut.")
            continue

        channel_id = input("Bitte gib die Kanal-ID der Lampe ein: ").strip()
        if not channel_id:
            print("Gültige Kanal-ID eingeben. Versuche es bitte erneut.")
            continue

        status = input("Möchtest du die Lampe ein- oder ausschalten? (an/aus): ").strip().lower()
        if status not in ["an", "aus"]:
            print("Ungültiger Status. Bitte 'an' oder 'aus' eingeben.")
            continue

        lampe_steuern(device_id, channel_id, status)

        nochmal = input("Möchtest du eine weitere Lampe steuern? (ja/nein): ").strip().lower()
        if nochmal != "ja":
            break

    print("Danke, dass du das Steuerungstool benutzt hast. Auf Wiedersehen!")


if __name__ == "__main__":
    main()
