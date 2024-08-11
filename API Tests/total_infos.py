import requests
import variabels
from requests.auth import HTTPBasicAuth

hostname = variabels.hostname
username = variabels.username
password = variabels.password

config_url = f'http://{hostname}/fhapi/v1/api/rest/configuration'


def drucke_sysap_info(sysap):
    print("SYSAP INFORMATIONEN:")
    print(f"Name: {sysap.get('sysapName', 'Nicht verfügbar')}")
    print(f"UART Seriennummer: {sysap.get('uartSerialNumber', 'Nicht verfügbar')}")
    print(f"Testmodus: {sysap.get('testMode', 'Nicht verfügbar')}")
    print(f"Version: {sysap.get('version', 'Nicht verfügbar')}")
    print(f"Sunrise Zeiten: {sysap.get('sunRiseTimes', 'Nicht verfügbar')}")
    print(f"Sunset Zeiten: {sysap.get('sunSetTimes', 'Nicht verfügbar')}")
    location = sysap.get('location', {})
    print(
        f"Standort: Breite={location.get('latitude', 'Nicht verfügbar')}, Länge={location.get('longitude', 'Nicht verfügbar')}")
    print("__________")


def drucke_floorplan_info(floorplan):
    print("FLOORPLAN:")
    for stockwerk_id, stockwerk in floorplan.get('floors', {}).items():
        print(f"  Stockwerk-ID: {stockwerk_id}")
        print(f"    Name: {stockwerk.get('name', 'Nicht verfügbar')}")
        print("    Räume:")
        for raum_id, raum in stockwerk.get('rooms', {}).items():
            print(f"      Raum-ID: {raum_id}")
            print(f"        Name: {raum.get('name', 'Nicht verfügbar')}")


def main():
    try:
        response = requests.get(
            config_url,
            auth=HTTPBasicAuth(username, password),
            verify=False
        )
        response.raise_for_status()
        config_daten = response.json()
        for sysap_uuid, sysap in config_daten.items():
            drucke_sysap_info(sysap.get('sysap', {}))
            drucke_floorplan_info(sysap.get('floorplan', {}))
    except requests.exceptions.RequestException as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()
