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


def drucke_geraete_info(geraete_id, geraet):
    print(f"Geräte-ID: {geraete_id}")
    print(f"Name: {geraet.get('displayName', 'Nicht verfügbar')}")
    print(f"Raum: {geraet.get('room', 'Nicht verfügbar')}")
    print(f"Stockwerk: {geraet.get('floor', 'Nicht verfügbar')}")
    print(f"Artikelnummer: {geraet.get('articleNumber', 'Nicht verfügbar')}")
    print(f"Schnittstelle: {geraet.get('interface', 'Nicht verfügbar')}")
    print(f"Native ID: {geraet.get('nativeId', 'Nicht verfügbar')}")
    print("Kanäle:")
    for kanal_id, kanal in geraet.get('channels', {}).items():
        print(f"  Kanal-ID: {kanal_id}")
        print(f"    Name: {kanal.get('displayName', 'Nicht verfügbar')}")
        print(f"    Funktion-ID: {kanal.get('functionID', 'Nicht verfügbar')}")
        print(f"    Raum: {kanal.get('room', 'Nicht verfügbar')}")
        print(f"    Stockwerk: {kanal.get('floor', 'Nicht verfügbar')}")
        print("    Eingänge:")
        for eingang_id, eingang_daten in kanal.get('inputs', {}).items():
            print(f"      Eingang-ID: {eingang_id}")
            print(f"        Pairing-ID: {eingang_daten.get('pairingID', 'Nicht verfügbar')}")
            print(f"        Wert: {eingang_daten.get('value', 'Nicht verfügbar')}")
        print("    Ausgänge:")
        for ausgang_id, ausgang_daten in kanal.get('outputs', {}).items():
            print(f"      Ausgang-ID: {ausgang_id}")
            print(f"        Pairing-ID: {ausgang_daten.get('pairingID', 'Nicht verfügbar')}")
            print(f"        Wert: {ausgang_daten.get('value', 'Nicht verfügbar')}")
        print("    Parameter:")
        for param_id, param_wert in kanal.get('parameters', {}).items():
            print(f"      Parameter-ID: {param_id}")
            print(f"        Wert: {param_wert}")


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
            for geraete_id, geraet in sysap.get('devices', {}).items():
                drucke_geraete_info(geraete_id, geraet)
            drucke_floorplan_info(sysap.get('floorplan', {}))
    except requests.exceptions.RequestException as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()
