from bs4 import BeautifulSoup
import html
import re


def parse_librus_with_improvements(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    rows = soup.find_all('tr', class_=['line0', 'line1'])

    for row in rows:
        cols = row.find_all('td', recursive=False)
        if len(cols) < 10:
            continue

        subject_name = cols[1].get_text(strip=True)
        if not subject_name or "Zachowanie" in subject_name:
            continue

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

        decoded_title = html.unescape(title_content)
        clean_title = re.sub(r'<br\s*/?>', '\n', decoded_title)

        details = {}
        for line in clean_title.split('\n'):
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                key, val = line.split(':', 1)
                details[key.strip().lower()] = val.strip()

        # LOGIKA ŁĄCZENIA POPRAW
        if 'poprawa oceny' in details and len(grades) > 0:
            # Pobieramy poprzednią ocenę z listy (to jest ocena pierwotna)
            ocena_pierwotna = grades.pop()

            # Tworzymy połączony obiekt
            combined_grade = {
                "typ": "poprawa",
                "ocena_tekst": f"Poprawa: {ocena_pierwotna['ocena']} / {ocena_wartosc}",
                "ocena_pierwotna": ocena_pierwotna['ocena'],
                "ocena_poprawiona": ocena_wartosc,
                "kategoria": details.get("kategoria", ocena_pierwotna.get("kategoria")),
                "data_pierwotna": ocena_pierwotna.get("data"),
                "data_poprawy": details.get("data"),
                "waga": details.get("waga", ocena_pierwotna.get("waga")),
                "szczegoly_pierwotne": ocena_pierwotna,
                "szczegoly_poprawione": details
            }
            grades.append(combined_grade)
        else:
            # Zwykła ocena
            details['typ'] = 'zwykła'
            details['ocena'] = ocena_wartosc
            grades.append(details)

    return grades


# --- Uruchomienie ---
with open('doc/oceny.html', 'r', encoding='utf-8') as f:
    html_data = f.read()

oceny = parse_librus_with_improvements(html_data)

# Wypisanie wyników
for p in oceny:
    print(f"\n{'=' * 40}")
    print(f"PRZEDMIOT: {p['przedmiot']}")
    print(f"{'=' * 40}")

    for okres_nazwa, okres_klucz in [("OKRES 1", "okres_1"), ("OKRES 2", "okres_2")]:
        print(f"\n--- {okres_nazwa} ---")
        if not p[okres_klucz]:
            print("Brak ocen.")
            continue

        for o in p[okres_klucz]:
            if o.get('typ') == 'poprawa':
                print(f"⭐ {o['ocena_tekst']}")
                print(f"     Kategoria: {o['kategoria']} (Waga: {o['waga']})")
                print(f"     Data 1. terminu: {o['data_pierwotna']}")
                print(f"     Data poprawy:    {o['data_poprawy']}")
            else:
                # Zwykła ocena
                ocena_val = o.get('ocena')
                # Zamiana "np" na czytelniejsze
                if ocena_val == "nieprzygotowany":
                    ocena_val = "np (nieprzygotowanie)"

                print(f"🔸 Ocena: {ocena_val}")
                print(f"     Kategoria: {o.get('kategoria', 'brak')} (Waga: {o.get('waga', 'brak')})")
                print(f"     Data: {o.get('data', 'brak')}")
                if 'komentarz' in o:
                    print(f"     Komentarz: {o['komentarz']}")