import sys
from bs4 import BeautifulSoup, Comment


def clean_librus_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    # 1. Usuwamy szum techniczny
    tags_to_remove = [
        'script', 'style', 'meta', 'link', 'noscript',
        'header', 'footer', 'select', 'input', 'form'
    ]
    for tag in soup.find_all(tags_to_remove):
        tag.decompose()

    # 2. Usuwamy komentarze HTML
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    body = soup.find('body')
    if not body:
        return "Błąd: Nie znaleziono sekcji <body>"

    # 3. Przetwarzanie ocen (Librus trzyma detale w atrybucie 'title' linków)
    # Zamieniamy linki z ocenami na tekst zawierający ich pełny opis
    for grade in body.find_all('a', class_='ocena'):
        title_data = grade.get('title', '')
        # Czyścimy tagi <br> z tooltipa na spacje
        clean_title = title_data.replace('<br>', ' | ').replace('<br/>', ' | ')
        grade_val = grade.get_text(strip=True)
        grade.replace_with(f"[{grade_val} ({clean_title})]")

    # 4. Iteracja po strukturze i budowanie czystego tekstu
    output = []

    # Interesuje nas głównie kontener z ocenami
    main_content = body.find('div', id='body') or body

    for element in main_content.descendants:
        if element.name in ['tr', 'div', 'p', 'h2', 'h3']:
            # Dodajemy nową linię dla strukturalnych elementów
            output.append('\n')

        if isinstance(element, str):
            text = element.strip()
            if text:
                output.append(text + ' ')

    # 5. Finalne czyszczenie białych znaków
    result = ' '.join(output)
    # Usuwamy wielokrotne spacje i puste linie
    import re
    result = re.sub(r' +', ' ', result)
    result = re.sub(r'\n\s*\n', '\n', result)

    return result.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python librus_parser.py sciezka_do_pliku.html")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='windows-1250') as f:
            content = f.read()
            clean_text = clean_librus_html(content)
            print(clean_text)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {file_path}")