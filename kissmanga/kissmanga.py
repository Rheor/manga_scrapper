import requests
from bs4 import BeautifulSoup

from kissmanga.config import (
    LIBRARY_PATH,
    DELAY,
    KISSMANGA_BASE_PATH,
    KISSMANGA_LIST_URL,
)
from kissmanga.helpers import create_dir
from kissmanga.mangas import process_single_manga

def kissmanga():
    url_content = requests.get(KISSMANGA_LIST_URL).text
    soup = BeautifulSoup(url_content, "html.parser")
    mangas_links = soup.find_all(name="a", attrs={"class": "item_movies_link"})

    for manga_link in mangas_links:
        relative_url = manga_link.get("href")
        manga_name = manga_link.text.replace(" ", "_")
        manga_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
        path_prefix = f"{LIBRARY_PATH}/{manga_name}"
        create_dir(path_prefix)
        process_single_manga(manga_url, path_prefix)