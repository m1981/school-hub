from bs4 import BeautifulSoup


def parse_librus_grades_robust(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # 1. Znajdź właściwą tabelę (szukamy takiej, która ma w nagłówku "Przedmiot")
    tables = soup.find_all('table')
    target_table = None

    for i, tbl in enumerate(tables):
        headers = tbl.get_text().lower()
        if "przedmiot" in headers and "okres 1" in headers:
            target_table = tbl
            print(f"[DEBUG] Znaleziono właściwą tabelę ocen (indeks {i}).")
            break

    if not target_table:
        print("[DEBUG] BŁĄD: Nie znaleziono tabeli zawierającej słowo 'Przedmiot'.")
        return []

    # 2. Pobierz wszystkie wiersze z tej tabeli
    rows = target_table.find_all('tr')
    print(f"[DEBUG] Tabela ma łącznie {len(rows)} wierszy (wliczając nagłówki i szczegóły).")

    # 3. Iteracja po wierszach
    for index, row in enumerate(rows):
        # Szukamy komórek td (pomijamy th - nagłówki)
        cols = row.find_all('td', recursive=False)

        # Interesują nas tylko wiersze, które mają co najmniej 8-9 kolumn (wiersze z przedmiotami)
        if len(cols) < 8:
            continue

        # Wyciągamy tekst z pierwszych kolumn, żeby zlokalizować nazwę przedmiotu
        col0_text = cols[0].get_text(strip=True)
        col1_text = cols[1].get_text(strip=True)
        col2_text = cols[2].get_text(strip=True)

        # Nazwa przedmiotu zazwyczaj jest w kolumnie 1, ale czasem w 0 (jeśli nie ma checkboxów)
        subject_name = col1_text if col1_text else col0_text

        if not subject_name or "Zachowanie" in subject_name or "Przedmiot" in subject_name:
            continue

        print(f"[DEBUG] Przetwarzam przedmiot: '{subject_name}' (Kolumny: {len(cols)})")

        try:
            # Na podstawie Twoich logów (9 kolumn), układ to zazwyczaj:
            # 0: Puste/Ikona, 1: Przedmiot, 2: Oceny I, 3: Średnia I, 4: Proponowana I, 5: Końcowa I, 6: Oceny II
            # Zabezpieczamy się przed błędem indeksu
            okres1_oceny = extract_grades_details(cols[2]) if len(cols) > 2 else []

            # Oceny na 2 semestr mogą być w kolumnie 5 lub 6 zależnie od ustawień szkoły
            # Szukamy kolumny, która ma w sobie linki <a> (czyli oceny)
            okres2_col_index = 6
            if len(cols) > 6 and not cols[6].find('a') and cols[5].find('a'):
                okres2_col_index = 5

            okres2_oceny = extract_grades_details(cols[okres2_col_index]) if len(cols) > okres2_col_index else []

            results.append({
                "przedmiot": subject_name,
                "okres_1": okres1_oceny,
                "okres_2": okres2_oceny
            })

        except Exception as e:
            print(f"[DEBUG] Błąd przy przedmiocie {subject_name}: {e}")

    return results


def extract_grades_details(td_cell):
    grades = []
    # Szukamy wszystkich tagów <a> (linków z ocenami)
    grade_links = td_cell.find_all('a')

    for link in grade_links:
        ocena = link.get_text(strip=True)
        title_content = link.get('title', '')

        if not ocena or not title_content:
            continue

        # Parsowanie tooltipa
        clean_title = title_content.replace('<br>', '\n').replace('<br/>', '\n')
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
try:
    with open('doc/oceny.html', 'r', encoding='windows-1250') as f:
        html_data = f.read()

    oceny_ucznia = parse_librus_grades_robust(html_data)

    print("\n=== WYNIKI KOŃCOWE ===")
    for p in oceny_ucznia:
        print(f"\n{p['przedmiot']}:")
        print(f"  Okres 1: {p['okres_1']}")
        print(f"  Okres 2: {p['okres_2']}")

except Exception as e:
    print(f"[BŁĄD KRYTYCZNY] {e}")