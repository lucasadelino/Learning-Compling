"""
This script scrapes Filmow's database and saves the film code of each film. A 
film code is a string of up to 6 digits that Filmow uses to identify each film.
Currently, each page in Filmow's catalog contains 24 films. 
Check out film_codes.txt for the output of this script. 
"""

import requests, bs4
from pathlib import Path
from pprint import pformat

# Number of pages to be scraped
MAX_PAGES = 100

page_number = 1
film_codes = []

while page_number <= MAX_PAGES:
    # Get request object for current page and generate soup object
    page = requests.get('https://filmow.com/filmes-todos/?pagina=' + str(page_number))
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    
    # Search for movies (which are <li> items in the HTML)
    tags = soup('li', class_='movie_list_item')

    # Populate list with film code (the value of the 'data-movie-pk' attribute)
    for element in tags:
        film_codes.append(element['data-movie-pk'])
    
    print('Got page number ' + str(page_number))

    page_number += 1

# Write film codes to a .py file. This way, it's easier to use chunks of the 
# list if you don't want or need to use everything.
with open(Path.cwd() / 'film_codes.py', 'w') as file:
    file.write('film_codes = ')
    file.write(pformat(film_codes))
