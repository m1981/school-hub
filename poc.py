from bs4 import BeautifulSoup
import re
import json


def parse_librus_grades(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # Znajdujemy główną tabelę ocen
    table = soup.select_one('table.decorated.stretch')
    if not table:
        return "Nie znaleziono tabeli ocen."

    # Iterujemy po wierszach przedmiotów (omijamy nagłówki)
    rows = table.select('tbody > tr.line0, tbody > tr.line1')

    for row in rows:
        cols = row.find_all('td', recursive=False)

        # Pomijamy wiersze rozwijane (szczegóły) i wiersz zachowania
        if len(cols) < 10 or "Zachowanie" in row.text:
            continue

        subject_name = cols[1].get_text(strip=True)

        # Okres 1 to kolumna 2, Okres 2 to kolumna 6
        # (Indeksy mogą się różnić zależnie od konfiguracji szkoły,
        # ale w tym HTML: 2=Oceny I, 5=Ocena I, 6=Oceny II)

        subject_data = {
            "przedmiot": subject_name,
            "okres_1": {
                "oceny_biezace": extract_grades_details(cols[2]),
                "srednia": "brak (blokada)" if "pomoc_ciemna.png" in str(cols[3]) else cols[3].get_text(strip=True),
                "proponowana": cols[4].get_text(strip=True),
                "finalna": cols[5].get_text(strip=True)
            },
            "okres_2": {
                "oceny_biezace": extract_grades_details(cols[6]),
                "srednia": "brak (blokada)" if "pomoc_ciemna.png" in str(cols[7]) else cols[7].get_text(strip=True),
                "finalna": cols[8].get_text(strip=True)
            }
        }
        results.append(subject_data)

    return results


def extract_grades_details(td_cell):
    """Wyciąga szczegóły każdej oceny z tooltipa (atrybut title)"""
    grades = []
    grade_boxes = td_cell.select('span.grade-box a')

    for box in grade_boxes:
        title_content = box.get('title', '')
        # Librus trzyma dane w formacie: Kategoria: XYZ<br>Data: ...
        # Czyścimy tagi <br> i dzielimy na linie
        clean_title = title_content.replace('<br>', '\n').replace('<br/>', '\n')

        details = {}
        lines = clean_title.split('\n')
        for line in lines:
            if ':' in line:
                key, val = line.split(':', 1)
                details[key.strip().lower()] = val.strip()

        grade_info = {
            "ocena": box.get_text(strip=True),
            "kategoria": details.get("kategoria", "brak"),
            "data": details.get("data", "brak"),
            "waga": details.get("waga", "1"),
            "nauczyciel": details.get("nauczyciel", "brak"),
            "komentarz": details.get("komentarz", "")
        }
        grades.append(grade_info)

    return grades


# --- Uruchomienie ---
# Zakładamy, że 'oceny.html' to Twój plik
with open('doc/oceny.html', 'r', encoding='utf-8') as f:
    html_data = f.read()

oceny_ucznia = parse_librus_grades(html_data)

# Wypisanie danych w czytelny sposób
for p in oceny_ucznia:
    print(f"\n=== {p['przedmiot']} ===")
    print(f"  [Okres 1] Ocena śródroczna: {p['okres_1']['finalna']}")
    for o in p['okres_1']['oceny_biezace']:
        print(f"    - {o['ocena']} (Waga: {o['waga']}, Kat: {o['kategoria']}, Data: {o['data']})")

    print(f"  [Okres 2]")
    for o in p['okres_2']['oceny_biezace']:
        print(f"    - {o['ocena']} (Waga: {o['waga']}, Kat: {o['kategoria']}, Data: {o['data']})")