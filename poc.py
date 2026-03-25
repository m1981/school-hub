from bs4 import BeautifulSoup


def parse_my_librus(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # Iterujemy po wierszach używając klas, które sam podałeś (line0 i line1)
    # Szukamy ich w całym dokumencie, co omija problem szukania właściwej tabeli
    rows = soup.find_all('tr', class_=['line0', 'line1'])

    for row in rows:
        cols = row.find_all('td', recursive=False)

        # Z Twojego kodu wynika, że wiersz przedmiotu ma 11 kolumn
        if len(cols) < 10:
            continue

        subject_name = cols[1].get_text(strip=True)

        # Pomijamy wiersze techniczne lub zachowanie
        if not subject_name or "Zachowanie" in subject_name:
            continue

        # Wyciągamy oceny z kolumny 2 (Okres 1) i kolumny 6 (Okres 2)
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
    # Szukamy linków z klasą 'ocena' (zgodnie z Twoim HTML: class="ocena")
    grade_links = td_cell.find_all('a', class_='ocena')

    for link in grade_links:
        ocena = link.get_text(strip=True)
        title_content = link.get('title', '')

        # Dekodowanie encji HTML (np. &lt;br&gt; na <br>)
        # BeautifulSoup robi to częściowo, ale w title Librus ma to podwójnie zakodowane
        clean_title = title_content.replace('&lt;br&gt;', '\n').replace('&lt;br/&gt;', '\n').replace('<br>',
                                                                                                     '\n').replace(
            '<br/>', '\n')

        details = {}
        for line in clean_title.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                details[key.strip().lower()] = val.strip()

        grades.append({
            "ocena": ocena,
            "kategoria": details.get("kategoria", "brak"),
            "data": details.get("data", "brak"),
            "waga": details.get("waga", "1")
        })
    return grades


# --- Uruchomienie ---
with open('doc/oceny.html', 'r', encoding='windows-1250') as f:
    html_data = f.read()

oceny = parse_my_librus(html_data)

for p in oceny:
    print(f"\n{p['przedmiot']}:")
    print(f"  Semestr 1: {[o['ocena'] for o in p['okres_1']]}")
    print(f"  Semestr 2: {[o['ocena'] for o in p['okres_2']]}")