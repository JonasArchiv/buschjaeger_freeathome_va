import requests
import variabels
from requests.auth import HTTPBasicAuth

hostname = variabels.hostname
username = variabels.username
password = variabels.password

config_url = f'http://{hostname}/fhapi/v1/api/rest/configuration'


def filter_und_drucke_informationen(daten, kategorie, suchbegriff, suchtyp):
    for sysap_uuid, sysap in daten.items():
        print(f"SysAP UUID: {sysap_uuid}")
        if kategorie == "device":
            for geraete_id, geraet in sysap.get('devices', {}).items():
                if suchtyp == "name" and suchbegriff.lower() in geraet.get('displayName', '').lower():
                    drucke_geraet_info(geraete_id, geraet, suchbegriff)
                elif suchtyp == "id" and suchbegriff.lower() == geraete_id.lower():
                    drucke_geraet_info(geraete_id, geraet, suchbegriff)
        elif kategorie == "room":
            for stockwerk_id, stockwerk in sysap.get('floorplan', {}).get('floors', {}).items():
                for raum_id, raum in stockwerk.get('rooms', {}).items():
                    if suchtyp == "name" and suchbegriff.lower() in raum.get('name', '').lower():
                        drucke_raum_info(raum_id, raum)
                    elif suchtyp == "id" and suchbegriff.lower() == raum_id.lower():
                        drucke_raum_info(raum_id, raum)


def drucke_geraet_info(geraete_id, geraet, suchbegriff):
    print(f"  Geräte-ID: {geraete_id}")
    print(f"    Name: {geraet.get('displayName', 'Nicht verfügbar')}")
    print(f"    Raum: {geraet.get('room', 'Nicht verfügbar')}")
    print(f"    Stockwerk: {geraet.get('floor', 'Nicht verfügbar')}")
    print(f"    Artikelnummer: {geraet.get('articleNumber', 'Nicht verfügbar')}")
    print(f"    Schnittstelle: {geraet.get('interface', 'Nicht verfügbar')}")
    print(f"    Native ID: {geraet.get('nativeId', 'Nicht verfügbar')}")
    kanaele = geraet.get('channels', {})
    if kanaele:
        print("    Kanäle:")
        for kanal_id, kanal in kanaele.items():
            if suchbegriff.lower() in kanal.get('displayName', '').lower():
                drucke_kanal_info(kanal_id, kanal)


def drucke_kanal_info(kanal_id, kanal):
    print(f"    Kanal-ID: {kanal_id}")
    print(f"      Name: {kanal.get('displayName', 'Nicht verfügbar')}")
    print(f"      Funktion-ID: {kanal.get('functionID', 'Nicht verfügbar')}")
    print(f"      Raum: {kanal.get('room', 'Nicht verfügbar')}")
    print(f"      Stockwerk: {kanal.get('floor', 'Nicht verfügbar')}")
    eingaenge = kanal.get('inputs', {})
    if eingaenge:
        print("      Eingänge:")
        for eingang_id, eingang_daten in eingaenge.items():
            print(f"        Eingang-ID: {eingang_id}")
            print(f"          Pairing-ID: {eingang_daten.get('pairingID', 'Nicht verfügbar')}")
            print(f"          Wert: {eingang_daten.get('value', 'Nicht verfügbar')}")
    ausgaenge = kanal.get('outputs', {})
    if ausgaenge:
        print("      Ausgänge:")
        for ausgang_id, ausgang_daten in ausgaenge.items():
            print(f"        Ausgang-ID: {ausgang_id}")
            print(f"          Pairing-ID: {ausgang_daten.get('pairingID', 'Nicht verfügbar')}")
            print(f"          Wert: {ausgang_daten.get('value', 'Nicht verfügbar')}")
    parameter = kanal.get('parameters', {})
    if parameter:
        print("      Parameter:")
        for param_id, param_wert in parameter.items():
            print(f"        Parameter-ID: {param_id}")
            print(f"          Wert: {param_wert}")


def drucke_raum_info(raum_id, raum):
    print(f"  Raum-ID: {raum_id}")
    print(f"    Name: {raum.get('name', 'Nicht verfügbar')}")


def main():
    try:
        response = requests.get(
            config_url,
            auth=HTTPBasicAuth(username, password),
            verify=False
        )
        response.raise_for_status()
        config_daten = response.json()
        kategorie = input("Wähle eine Kategorie (device/room): ").strip().lower()
        suchbegriff = input("Gib den Suchbegriff ein: ").strip()
        suchtyp = input("Suchtyp (name/id): ").strip().lower()
        if kategorie not in ["device", "room"]:
            print("Ungültige Kategorie. Bitte 'device' oder 'room' wählen.")
            return
        if suchtyp not in ["name", "id"]:
            print("Ungültiger Suchtyp. Bitte 'name' oder 'id' wählen.")
            return
        filter_und_drucke_informationen(config_daten, kategorie, suchbegriff, suchtyp)
    except requests.exceptions.RequestException as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()
