import requests
import variabels
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime

hostname = variabels.hostname
username = variabels.username
password = variabels.password

config_url = f'http://{hostname}/fhapi/v1/api/rest/configuration'


def filter_und_drucke_informationen(daten, kategorie, suchbegriff, suchtyp):
    output_lines = []
    for sysap_uuid, sysap in daten.items():
        output_lines.append(f"SysAP UUID: {sysap_uuid}")
        if kategorie == "device":
            for geraete_id, geraet in sysap.get('devices', {}).items():
                if suchtyp == "name" and suchbegriff.lower() in geraet.get('displayName', '').lower():
                    output_lines.extend(drucke_geraet_info(geraete_id, geraet, suchbegriff))
                elif suchtyp == "id" and suchbegriff.lower() == geraete_id.lower():
                    output_lines.extend(drucke_geraet_info(geraete_id, geraet, suchbegriff))
        elif kategorie == "room":
            for stockwerk_id, stockwerk in sysap.get('floorplan', {}).get('floors', {}).items():
                for raum_id, raum in stockwerk.get('rooms', {}).items():
                    if suchtyp == "name" and suchbegriff.lower() in raum.get('name', '').lower():
                        output_lines.extend(drucke_raum_info(raum_id, raum))
                    elif suchtyp == "id" and suchbegriff.lower() == raum_id.lower():
                        output_lines.extend(drucke_raum_info(raum_id, raum))
    return output_lines


def drucke_geraet_info(geraete_id, geraet, suchbegriff):
    output_lines = []
    output_lines.append(f"  Geräte-ID: {geraete_id}")
    output_lines.append(f"    Name: {geraet.get('displayName', 'Nicht verfügbar')}")
    output_lines.append(f"    Raum: {geraet.get('room', 'Nicht verfügbar')}")
    output_lines.append(f"    Stockwerk: {geraet.get('floor', 'Nicht verfügbar')}")
    output_lines.append(f"    Artikelnummer: {geraet.get('articleNumber', 'Nicht verfügbar')}")
    output_lines.append(f"    Schnittstelle: {geraet.get('interface', 'Nicht verfügbar')}")
    output_lines.append(f"    Native ID: {geraet.get('nativeId', 'Nicht verfügbar')}")
    kanaele = geraet.get('channels', {})
    if kanaele:
        output_lines.append("    Kanäle:")
        for kanal_id, kanal in kanaele.items():
            if suchbegriff.lower() in kanal.get('displayName', '').lower():
                output_lines.extend(drucke_kanal_info(kanal_id, kanal))
    return output_lines


def drucke_kanal_info(kanal_id, kanal):
    output_lines = []
    output_lines.append(f"    Kanal-ID: {kanal_id}")
    output_lines.append(f"      Name: {kanal.get('displayName', 'Nicht verfügbar')}")
    output_lines.append(f"      Funktion-ID: {kanal.get('functionID', 'Nicht verfügbar')}")
    output_lines.append(f"      Raum: {kanal.get('room', 'Nicht verfügbar')}")
    output_lines.append(f"      Stockwerk: {kanal.get('floor', 'Nicht verfügbar')}")
    eingaenge = kanal.get('inputs', {})
    if eingaenge:
        output_lines.append("      Eingänge:")
        for eingang_id, eingang_daten in eingaenge.items():
            output_lines.append(f"        Eingang-ID: {eingang_id}")
            output_lines.append(f"          Pairing-ID: {eingang_daten.get('pairingID', 'Nicht verfügbar')}")
            output_lines.append(f"          Wert: {eingang_daten.get('value', 'Nicht verfügbar')}")
    ausgaenge = kanal.get('outputs', {})
    if ausgaenge:
        output_lines.append("      Ausgänge:")
        for ausgang_id, ausgang_daten in ausgaenge.items():
            output_lines.append(f"        Ausgang-ID: {ausgang_id}")
            output_lines.append(f"          Pairing-ID: {ausgang_daten.get('pairingID', 'Nicht verfügbar')}")
            output_lines.append(f"          Wert: {ausgang_daten.get('value', 'Nicht verfügbar')}")
    parameter = kanal.get('parameters', {})
    if parameter:
        output_lines.append("      Parameter:")
        for param_id, param_wert in parameter.items():
            output_lines.append(f"        Parameter-ID: {param_id}")
            output_lines.append(f"          Wert: {param_wert}")
    return output_lines


def drucke_raum_info(raum_id, raum):
    output_lines = []
    output_lines.append(f"  Raum-ID: {raum_id}")
    output_lines.append(f"    Name: {raum.get('name', 'Nicht verfügbar')}")
    return output_lines


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

        output_lines = filter_und_drucke_informationen(config_daten, kategorie, suchbegriff, suchtyp)

        for line in output_lines:
            print(line)

        os.makedirs('search_output', exist_ok=True)

        datum = datetime.now().strftime("%Y%m%d_%H%M%S")
        dateiname = f"{kategorie}_{suchbegriff}_{suchtyp}_{datum}.txt"
        pfad = os.path.join('search_output', dateiname)

        with open(pfad, 'w', encoding='utf-8') as file:
            for line in output_lines:
                file.write(line + '\n')

        print(f"Die Ergebnisse wurden in der Datei '{pfad}' gespeichert.")

    except requests.exceptions.RequestException as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()
