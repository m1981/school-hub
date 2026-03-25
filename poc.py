from bs4 import BeautifulSoup
import html
import re


def parse_librus_full_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # Szukamy wierszy z klasami line0 i line1
    rows = soup.find_all('tr', class_=['line0', 'line1'])

    for row in rows:
        cols = row.find_all('td', recursive=False)

        # Upewniamy się, że to wiersz przedmiotu (11 kolumn)
        if len(cols) < 10:
            continue

        subject_name = cols[1].get_text(strip=True)
        if not subject_name or "Zachowanie" in subject_name:
            continue

        # Wyciągamy oceny z odpowiednich kolumn
        okres1_oceny = extract_grades(cols[2])
        okres2_oceny = extract_grades(cols[6])

        results.append({
            "przedmiot": subject_name,
            "okres_1": okres1_oceny,
            "okres_2": okres2_oceny
        })

    return results


def extract_grades(td_cell):
    grades = []
    grade_links = td_cell.find_all('a', class_='ocena')

    for link in grade_links:
        ocena_wartosc = link.get_text(strip=True)
        title_content = link.get('title', '')

        if not ocena_wartosc or not title_content:
            continue

        # 1. Odkodowanie encji HTML (zamienia &lt;br&gt; na <br>)
        decoded_title = html.unescape(title_content)

        # 2. Zamiana wszystkich wariantów <br>, <br/>, <br /> na znak nowej linii \n
        clean_title = re.sub(r'<br\s*/?>', '\n', decoded_title)

        # 3. Parsowanie klucz: wartość
        details = {"ocena": ocena_wartosc}

        for line in clean_title.split('\n'):
            line = line.strip()
            if not line:
                continue  # Pomijamy puste linie

            if ':' in line:
                # Dzielimy tylko po pierwszym dwukropku (bo w dacie lub komentarzu mogą być kolejne)
                key, val = line.split(':', 1)
                # Zapisujemy do słownika (klucze zamieniamy na małe litery dla spójności)
                details[key.strip().lower()] = val.strip()

        grades.append(details)

    return grades


# --- Uruchomienie ---
with open('doc/oceny.html', 'r', encoding='utf-8') as f:
    html_data = f.read()

oceny = parse_librus_full_details(html_data)

# Wypisanie wyników w czytelnej formie
for p in oceny:
    print(f"\n{'=' * 40}")
    print(f"PRZEDMIOT: {p['przedmiot']}")
    print(f"{'=' * 40}")

    print("\n--- OKRES 1 ---")
    if not p['okres_1']:
        print("Brak ocen.")
    for o in p['okres_1']:
        print(f"Ocena: {o.get('ocena')}")
        for key, value in o.items():
            if key != 'ocena':
                print(f"  - {key.capitalize()}: {value}")

    print("\n--- OKRES 2 ---")
    if not p['okres_2']:
        print("Brak ocen.")
    for o in p['okres_2']:
        print(f"Ocena: {o.get('ocena')}")
        for key, value in o.items():
            if key != 'ocena':
                print(f"  - {key.capitalize()}: {value}")