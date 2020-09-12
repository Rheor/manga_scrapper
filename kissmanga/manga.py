import time
import requests
from bs4 import BeautifulSoup

from kissmanga import Aggregator
from kissmanga.config import (
    KISSMANGA_BASE_PATH,
    MANGA_NAVIGATION_PARAMS
)
from kissmanga.helpers import create_dir
from kissmanga.chapters import ChapterAggregator


class MangaAggregator(Aggregator):

    def __init__(self, navigation_url, path_prefix, navigation_params_placeholder=MANGA_NAVIGATION_PARAMS):
        super().__init__(navigation_url)
        self.navigation_url = navigation_url
        self.navigation_params_placeholder = navigation_params_placeholder
        self.path_prefix = path_prefix

    def _scrap_page_content(self):
        chapters = self.soup.find_all(lambda tag: "chapter" in tag.attrs.get("href", ""))
        
        for chapter in chapters:
            relative_url = chapter.attrs["href"]
            chapter = relative_url.split("/")[-1]
            chapter_path_prefix = f"{self.path_prefix}/{chapter}"
            create_dir(chapter_path_prefix)
            chapter_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
            ChapterAggregator(chapter_url, chapter_path_prefix).aggregate_content()
            time.sleep(1)

    def aggregate_content(self):
        self._scrap_page_content()