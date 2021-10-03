"""
This script scrapes the comment section of a Filmow film. It searches for 
either negative (<= 2 stars out of five) or positive (>= 3 stars) reviews and
captures the comment text of the review. It then saves all comments in a .txt 
file.
"""

import requests, bs4, re
from pathlib import Path

# The rating of a review in Filmow is a <span> element whose title is always
# "Nota: X estrela(s)", where X can be a number between 0 and 5, optionally 
# followed by a .5 (for half-star ratings). The regexes below match negative or 
# positive reviews based on these criteria
negativo_regex = re.compile(r"Nota: ([0-1](\.5)?|2) e")
positivo_regex = re.compile(r"Nota: ([3-5](\.5)?) e")

# Each comment will be delimited by a \n character at the start and end of the 
# comment. Comments, however, may have additional \n characters if the author
# wrote multiple paragraphs. This regex will get rid of those "inner" \n's 
# while preserving the \n's at the start and end of the comment. This makes it
# easier to write comments to (and read them from) a .txt file
espaco_interno_regex = re.compile(r"(?<!^)(\n)(?!$)")

# Filmow will use the string below to display a comment made by a banned user
# These don't contain any meaningful data, so we'll ignore them
ignore_string = 'Usuário temporariamente bloqueado por infringir os termos de uso do Filmow.'

# Paste the codes of the films you want to scrape into this list
film_codes = ['284498', '260086', '328606', '281505', '268315', '284354', 
              '268698', '213025', '231751', '222762']

with open(Path.cwd() / 'negativo.txt', 'a', encoding='utf-8') as file:
    for i, film_code in enumerate(film_codes):
        has_next = True
        page_number = 1
        string_list = []

        while has_next != False:
            # Generate request object
            page = requests.get(f'https://filmow.com/async/comments/?content_type=22&object_pk={film_code}&user=all&order_by=-created&page={page_number}')
            page.raise_for_status()

            # Output console mesage to ensure script is running smoothly
            print(f'Getting film {i+1}, page {page_number}')
            
            # The request above will lead to a .JSON with two key-value pairs: 
            # {pagination: {DICT}, html: "CODE"}, where {DICT} ==
            # {has_next: BOOL, has_previous: BOOL, current_page: X}

            # Get HTML and pagination status from .JSON; Generate soup object
            html = page.json()['html']
            has_next = page.json()['pagination']['has_next']
            soup = bs4.BeautifulSoup(html, 'lxml')
            
            # Search for elements whose title equals our regex 
            tags = soup(title=negativo_regex)

            for element in tags:
                # Each of our tags is a rating (a <span> element). What we want  
                # is the comment text associated with that rating, so we need
                # to walk up and sideways in the soup tree accordingly
                text = element.parent.parent.find_previous_sibling().get_text()
                
                # Do this only if text != banned user message (ignore_string)
                if not ignore_string in text:
                    # Get rid of "inner" \n characters
                    text = espaco_interno_regex.sub(' ', text)
                    string_list.append(text)

            page_number += 1

        # Write to file and display confirmation console message
        file.write(''.join(string_list))
        print(f'Got film {i+1}/{len(film_codes)}')
