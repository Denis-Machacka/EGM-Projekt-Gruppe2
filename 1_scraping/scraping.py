import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time

# URL der Webseite, die wir scrapen wollen
base_url = 'https://www.immoscout24.ch/de/immobilien/mieten/kanton-zuerich'
page_num_suffix = '?pn='
page_num = 1

# Array, um die gesammelten Daten zu speichern
properties = []

while True:
    # URL für die aktuelle Seite erstellen
    url = base_url + (page_num_suffix + str(page_num) if page_num > 1 else '')

    print(f'Suche auf URL {url}')

    # Anfrage versenden
    response = requests.get(url)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite {url}. Statuscode: {response.status_code}")
        break

    # BeautifulSoup-Objekt erstellen, um die Seite zu parsen
    soup = BeautifulSoup(response.text, 'html.parser')

    # Immobiliencontainer auf der Seite finden
    property_list = soup.find_all('div', class_='HgListingCard_info_RKrwz')

    # Überprüfen, ob Immobilien gefunden wurden
    if not property_list:
        print('Keine Elemente gefunden, letzte Seite wahrscheinlich erreicht')
        break

    # Immobilien durchlaufen und Daten sammeln
    for property in property_list:
        # Titel, Preis, Zimmer, etc. extrahieren.
        title = property.find('div', class_='HgListingRoomsLivingSpacePrice_roomsLivingSpacePrice_M6Ktp').text.strip() if property.find('div', class_='HgListingRoomsLivingSpacePrice_roomsLivingSpacePrice_M6Ktp') else 'N/A'

        # Adresse extrahieren
        address_raw = property.find('address').text.strip() if property.find('address') else 'N/A'

        # Reguläre Ausdrücke für die gesuchten Daten innerhalb der Elemente
        zimmer_pattern = re.compile(r'(\d+\.?\d*) Zimmer')
        quadratmeter_pattern = re.compile(r'(\d+)m²')
        preis_pattern = re.compile(r'CHF ([\d’]+)')
        address_pattern = re.compile(r'(.+), (\d{4}) (.+)')

        # Suche nach den Daten im String
        zimmer = zimmer_pattern.search(title)
        quadratmeter = quadratmeter_pattern.search(title)
        preis = preis_pattern.search(title)
        match = address_pattern.search(address_raw)

        # Extrahiere und konvertiere die Daten
        zimmer = float(zimmer.group(1)) if zimmer else None
        quadratmeter = int(quadratmeter.group(1)) if quadratmeter else None
        preis = int(preis.group(1).replace('’', '')) if preis else None
        address = match.group(1) if match else None
        plz = match.group(2) if match else None
        ort = match.group(3) if match else None

        # Extrahierten Daten zum Array hinzufügen
        properties.append({
            'Zimmer': zimmer,
            'Quadratmeter': quadratmeter,
            'Preis': preis,
            'Adresse': address,
            'PLZ': plz,
            'Ort': ort
        })

    # Nächste Seite vorbereiten
    page_num += 1
    # Eine Pause einfügen, um zu vermeiden, die Website zu überlasten
    time.sleep(1)

# Ausgabe der gesammelten Daten
for prop in properties:
    print(prop)

# Pfad zur Zieldatei
dir_name = os.path.dirname(__file__)
file_path = os.path.join(dir_name, 'wohnungen_raw.csv')

# Zieldatei befüllen
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=properties[0].keys())

    writer.writeheader()

    for prop in properties:
        writer.writerow(prop)

print("Scraping abgeschlossen. Daten wurden in die CSV-Datei geschrieben.")
