import requests, bs4
from pathlib import Path
from pprint import pformat

MAX_PAGES = 100

page_number = 1
film_codes = []

while page_number <= MAX_PAGES:
    page = requests.get('https://filmow.com/filmes-todos/?pagina=' + str(page_number))
    page.raise_for_status()

    soup = bs4.BeautifulSoup(page.text, 'lxml')
    tags = soup('li', class_='movie_list_item')

    for element in tags:
        film_codes.append(element['data-movie-pk'])
    
    print('Got page number ' + str(page_number))

    page_number += 1

with open(Path.cwd() / 'film_codes.py', 'w') as file:
    file.write('film_codes = ')
    file.write(pformat(film_codes))
