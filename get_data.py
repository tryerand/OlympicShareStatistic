import requests
from bs4 import BeautifulSoup
import time
import json


def scrape_olympic_data(edition_ids):
    results = []

    ohne_jahr = []
    for i in edition_ids:
        url = f"https://www.olympedia.org/editions/{i}"
        print(f"Scrape Edition {i}...")

        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Austragungsort (Host City) extrahieren
        # Wir suchen das <th> mit Text "Host city" und nehmen das nächste <td>
        host_city = "Unbekannt"
        host_header = soup.find("th", string="Host city")
        if host_header:
            host_city = host_header.find_next_sibling("td").get_text(strip=True)

        year = "Unklar"
        year_el = soup.find("th", string="Number and Year")
        if year_el:
            year = year_el.find_next_sibling("td").get_text(strip=True).split(" / ")[1]
        else:
            ohne_jahr.append(i)
            continue
        # 2. Medaillenspiegel extrahieren

        medal_dict = {}
        medal_table_title = soup.find("h2", string="Medal table")
        if medal_table_title:
            table = medal_table_title.find_next_sibling("table")
        rows = table.find_all("tr")
        insgesamt_medals = 0
        for row in rows:
            cols = row.find_all("td")
            # Wir brauchen mindestens 6 Spalten (Index 0 bis 5)
            if len(cols) >= 6:
                country_name = cols[0].get_text(strip=True)
                # Index 5 ist das 6. <td> (Total Medals)
                total_medals = cols[5].get_text(strip=True)
                insgesamt_medals += int(total_medals)

                # Nur hinzufügen, wenn ein Ländername existiert (verhindert leere Zeilen)
                if country_name:
                    medal_dict[country_name] = total_medals

        # Daten speichern
        result = {
            "edition_id": i,
            "host_city": host_city,
            "year": year,
            "medals": medal_dict,
            "insgesamt_medals": insgesamt_medals
        }
        results.append(result)
        print(i, result)

        # Kurze Pause, um den Server nicht zu überlasten
        time.sleep(5)

        #except Exception as e:
        #    print(f"Fehler bei ID {i}: {e}")

    print("Ohne Jahr: " + str(ohne_jahr))
    return results


# Beispielaufruf für einige Editionen (z.B. 1=1896, 7=1920, 61=2022)
# Du kannst hier die gewünschten IDs in die Liste eintragen
test_ids = range(0, 73)
data = scrape_olympic_data(test_ids)

# Ausgabe der Ergebnisse
data = json.dumps(data, indent=4, ensure_ascii=False)
with open("daten.json", "w") as f:
    f.write(data)