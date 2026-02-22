import json
import matplotlib.pyplot as plt
import os

# 1. Daten laden
# Falls die Datei anders heißt, passe den Namen hier an
file_path = "daten.json"
if not os.path.exists(file_path):
    print(f"Datei {file_path} nicht gefunden!")
else:
    with open(file_path, "r", encoding="latin-1") as f:
        data = json.load(f)

    # 2. Daten chronologisch nach Jahr und ID sortieren
    # Das Jahr wird als Integer behandelt, um 1900 vor 2000 zu sortieren
    data.sort(key=lambda x: (int(x['year']) if x['year'].isdigit() else 0, x['edition_id']))

    # 3. Alle Länder sammeln
    all_countries = set()
    for edition in data:
        all_countries.update(edition["medals"].keys())

    # Ordner für Grafiken erstellen
    if not os.path.exists("olympia_plots"):
        os.makedirs("olympia_plots")

    # 4. Plots generieren
    for country in sorted(all_countries):
        x_labels = []
        medals_y = []
        bar_colors = []

        has_data = False
        for edition in data:
            if country in edition["medals"]:
                has_data = True
                # X-Achsen Label: Jahr und Ort
                label = f"{edition['year']} ({edition['edition_id']})"
                x_labels.append(label)

                # Medaillen als Integer
                m_count = float(edition["medals"][country]) / float(edition["insgesamt_medals"])

                medals_y.append(m_count)

                # Heimspiel-Check: Ist der Ländername im Host-City-String enthalten?
                # Wir prüfen, ob der Ländername (z.B. "Germany") im Host-String vorkommt.
                if country.lower() in edition["host_city"].lower():
                    bar_colors.append("red")
                else:
                    bar_colors.append("blue")

        if has_data:
            plt.figure(figsize=(14, 6))
            bars = plt.bar(x_labels, medals_y, color=bar_colors, edgecolor='black', alpha=0.8)

            plt.title(f"Medal Share development: {country}", fontsize=16, fontweight='bold')
            plt.xlabel("Year (Edition ID)", fontsize=12)
            plt.ylabel("Medal-share", fontsize=12)
            plt.xticks(rotation=90, fontsize=9)
            plt.grid(axis='y', linestyle='--', alpha=0.6)

            # Legende
            from matplotlib.lines import Line2D

            legend_elements = [Line2D([0], [0], color='blue', lw=4, label='Abroad'),
                               Line2D([0], [0], color='red', lw=4, label='At home')]
            plt.legend(handles=legend_elements)

            plt.tight_layout()

            # Speichern statt nur anzeigen (verhindert 200+ Fenster)
            filename = country.replace(" ", "_").replace("/", "_")
            plt.savefig(f"olympia_plots/{filename}.png")
            plt.close()  # Speicher freigeben

    print(f"Fertig! Alle Grafiken wurden im Ordner 'olympia_plots' gespeichert.")