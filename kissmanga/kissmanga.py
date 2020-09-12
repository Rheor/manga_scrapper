import requests
from bs4 import BeautifulSoup

from kissmanga.config import (
    LIBRARY_PATH,
    DELAY,
    KISSMANGA_BASE_PATH,
    KISSMANGA_LIST_URL,
    MANGA_NAVIGATION_PARAMS
)
from kissmanga import Aggregator
from kissmanga.helpers import create_dir
from kissmanga.manga import MangaAggregator

class KissmangaAggregator(Aggregator):

    def __init__(self, navigation_url, navigation_params_placeholder=MANGA_NAVIGATION_PARAMS):
        self.page_num = 1
        self.navigation_params_placeholder = navigation_params_placeholder
        self.navigation_url = navigation_url
        super().__init__(self._get_page_url())
        self.last_page = self._get_last_page()

    def _get_page_url(self):
        page_params = self.navigation_params_placeholder.format(self.page_num)
        return f"{self.navigation_url}{page_params}"

    def _get_last_page(self):
        print(self.navigation_url)
        last_url = self.soup.find_all("ul")[-1]
        last_page_link = [
            tag 
            for tag in list(last_url.children)
            if tag != "\n" and "Last" in getattr(tag, "text")
        ][0]
        last_page = int(last_page_link.text.replace("Last (", "").replace(") ", ""))
        return last_page

    def _scrap_page_content(self):
        mangas_links = self.soup.find_all(name="a", attrs={"class": "item_movies_link"})

        for manga_link in mangas_links:
            relative_url = manga_link.get("href")
            manga_name = "".join(char for char in manga_link.text if char.isalnum())
            manga_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
            path_prefix = f"{LIBRARY_PATH}/{manga_name}"
            create_dir(path_prefix)
            MangaAggregator(manga_url, path_prefix).aggregate_content()

    def _paginate(self):
        self.page_num += 1
        raw_content = requests.get(self._get_page_url()).text
        self.soup = BeautifulSoup(raw_content, "html.parser")
        return self.page_num < self.last_page

    def aggregate_content(self):
        while self._paginate():
            self._scrap_page_content()


def kissmanga():
    KissmangaAggregator(KISSMANGA_LIST_URL).aggregate_content()