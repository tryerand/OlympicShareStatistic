import json

# 1. Daten laden
file_path = "daten.json"
with open(file_path, "r", encoding="latin-1") as f:
    data = json.load(f)

# 2. Hilfsdaten strukturieren
countries = set()
for edition in data:
    countries.update(edition["medals"].keys())

# Wir speichern für jedes Land zwei Listen mit Medal Shares
stats = {country: {"home_shares": [], "away_shares": []} for country in countries}

for edition in data:
    # Gesamtanzahl der Medaillen in dieser Edition berechnen
    total_medals_in_edition = sum(int(m) for m in edition["medals"].values())
    if total_medals_in_edition == 0:
        continue

    for country in countries:
        if country in edition["medals"]:
            # Prozentualer Anteil (Share) berechnen
            share = int(edition["medals"][country]) / total_medals_in_edition

            # Prüfen, ob Heimspiel
            if country.lower() in edition["host_city"].lower():
                print("Gefunden", country.lower())
                stats[country]["home_shares"].append(share)
            else:
                stats[country]["away_shares"].append(share)
        else:
            # Wenn ein Land teilnimmt, aber 0 Medaillen hat, könnte man 0 anhängen.
            # Für diese Statistik zählen wir aber nur Editionen, in denen das Land aktiv war.
            pass

# 3. Verhältnisse berechnen
host_ratios = {}

for country, values in stats.items():
    # Nur Länder betrachten, die mindestens einmal Gastgeber waren
    if values["home_shares"]:
        avg_home = sum(values["home_shares"]) / len(values["home_shares"])

        # Nur berechnen, wenn das Land auch jemals auswärts Medaillen geholt hat
        if values["away_shares"] and sum(values["away_shares"]) > 0:
            avg_away = sum(values["away_shares"]) / len(values["away_shares"])
            ratio = avg_home / avg_away

            host_ratios[country] = {
                "ratio": round(ratio, 2),
                "avg_share_home": round(avg_home * 100, 2),  # in Prozent
                "avg_share_away": round(avg_away * 100, 2),  # in Prozent
                "host_count": len(values["home_shares"])
            }

# 4. Sortiert ausgeben (höchster Heimvorteil zuerst)
sorted_ratios = dict(sorted(host_ratios.items(), key=lambda item: item[1]['ratio'], reverse=True))

# Ergebnis als JSON speichern
with open("host_advantage_ratios.json", "w", encoding="utf-8") as f:
    json.dump(sorted_ratios, f, indent=4, ensure_ascii=False)

# Vorschau in der Konsole
print(f"{'Land':<20} | {'Heim-Quote (%)':<15} | {'Auswärts-Quote (%)':<15} | {'Faktor (Ratio)'}")
print("-" * 75)
durchschnittsvorteil_alle_länder = 0
count = 0
for country, v in list(sorted_ratios.items()):  # Top 15
    print(f"{country:<20} | {v['avg_share_home']:>14}% | {v['avg_share_away']:>14}% | {v['ratio']:>12}")
    durchschnittsvorteil_alle_länder += v["ratio"]
    count += 1
durchschnittsvorteil_alle_länder /= count
print("Durchschnittsvorteil: ", durchschnittsvorteil_alle_länder)
