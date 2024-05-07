import requests
from bs4 import BeautifulSoup


# URL of the IMDb page to scrape
URL = 'https://www.imdb.com/title/tt6084202/'

# Here we basicly mimic the URL trying to make the Browser think we are Legit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# GET request to the URL and parsing the HTML content
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# Director from the page
director_section = soup.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link', href=True)
if director_section:
    director = director_section.text.strip()

# Writers from the page
writter_section = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link', )
if writter_section:
    writter = writter_section[1].text.strip()
    writter1 = writter_section[2].text.strip()

# Actor if it's mentioned in the actor section
actor_section = soup.find('div', class_='sc-bfec09a1-7 gWwKlt')
if actor_section:
    actors = actor_section.find_all('a')
    for actor in actors:
        if "Oto Brantevics" in actor.text:
            actor_name = actor.text.strip()

# Awards and nominations
award_section = soup.find('span', class_="ipc-metadata-list-item__list-content-item")
for award in award_section:
    if "9 wins" in award.text:
        wins_nominations = award.text.strip()

print(f"Director: {director}")
print(f"Writters: {writter}, {writter1}")
print(f'Actor: {actor_name}')
print(f'Award: {wins_nominations}')