import requests, bs4, re
from pathlib import Path

negativo_regex = re.compile(r"Nota: ([0-1](\.5)?|2) e")
positivo_regex = re.compile(r"Nota: ([3-5](\.5)?) e")
espaco_interno_regex = re.compile(r"(?<!^)(\n)(?!$)")

film_codes = ['284498', '260086', '328606']

with open(Path.cwd() / 'positivos.txt', 'a', encoding='utf-8') as file:
    for i, film_code in enumerate(film_codes):
        has_next = True
        page_number = 1
        string_list = []

        while has_next != False:
            page = requests.get(f'https://filmow.com/async/comments/?content_type=22&object_pk={film_code}&user=all&order_by=-created&page={page_number}')
            page.raise_for_status()
            
            textie = page.json()['html']
            has_next = page.json()['pagination']['has_next']
            soup = bs4.BeautifulSoup(textie, 'lxml')
            tags = soup(title=positivo_regex)

            for element in tags:
                text = element.parent.parent.find_previous_sibling().get_text()
                text = espaco_interno_regex.sub(' ', text)
                string_list.append(text)
            
            page_number += 1

        file.write(''.join(string_list))
        print(f'Got film {i+1}/{len(film_codes)}')
