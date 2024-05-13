import pandas as pd
import os

def replace_umlauts(text):
    """ Ersetzt deutsche Umlaute in einem gegebenen Text. """
    replacements = {
        'ä': 'ae',
        'ü': 'ue',
        'ö': 'oe',
        'Ä': 'Ae',
        'Ü': 'Ue',
        'Ö': 'Oe'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text

# Setze den absoluten Pfad zur CSV-Datei
dir_name = os.path.dirname(os.path.abspath(__file__))
file_path_raw = os.path.join(dir_name, 'wohnungen_raw.csv')
file_path_clean = os.path.join(dir_name, 'wohnungen_clean.csv')

# Versuche, die Daten einzulesen
try:
    data = pd.read_csv(file_path_raw)
    print("Daten erfolgreich geladen!")
except FileNotFoundError:
    print(f"Datei nicht gefunden: {file_path_raw}")
    exit()

# Überprüfe auf fehlende Werte und zeige sie an
print("Anzahl fehlender Werte pro Spalte:")
print(data.isnull().sum())

# Fehlende Werte entfernen: Betrachte nur die notwendigen Spalten
data = data.dropna(subset=['Quadratmeter', 'Preis', 'Adresse', 'PLZ', 'Ort'])

# Duplikate entfernen
data = data.drop_duplicates()

# Konvertiere Datentypen, sicherstellen, dass keine Konvertierungsfehler auftreten
try:
    data['Quadratmeter'] = data['Quadratmeter'].astype(int)
    data['Preis'] = data['Preis'].astype(int)
    data['PLZ'] = data['PLZ'].astype(int)
except ValueError as e:
    print("Fehler bei der Datentypkonvertierung:", e)
    exit()

# Ersetze Umlaute in allen textbasierten Spalten
for column in data.select_dtypes(include=[object]).columns:
    data[column] = data[column].apply(replace_umlauts)

# Berechne den Preis pro Quadratmeter und runde auf zwei Dezimalstellen
data['Preis_pro_Quadratmeter'] = (data['Preis'] / data['Quadratmeter']).round(2)

# Kombiniere 'Adresse' und 'PLZ' in ein neues Attribut 'Adresse_PLZ'
data['Adresse_PLZ'] = data['Adresse'] + ', ' + data['PLZ'].astype(str)

# Füge das neue Attribut 'Kanton' hinzu und setze es auf 'Zurich' für alle Einträge
data['Kanton'] = 'Zurich'

# Definiere die gewünschte Spaltenreihenfolge
columns_order = ['Zimmer', 'Quadratmeter', 'Preis', 'Preis_pro_Quadratmeter', 'Adresse', 'PLZ', 'Ort', 'Kanton', 'Adresse_PLZ']

# Reorganisiere die Spalten gemäß der festgelegten Reihenfolge
data = data[columns_order]

# Überprüfe die bereinigten Daten und Datentypen
print("Bereinigte Daten:")
print(data.head())
print("\nDatentypen der Spalten:")
print(data.dtypes)

# Speichere die bereinigten Daten in einer neuen CSV-Datei
data.to_csv(file_path_clean, index=False)
print(f"Bereinigung abgeschlossen. Daten wurden in '{file_path_clean}' geschrieben.")
