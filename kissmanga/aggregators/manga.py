import time
import asyncio
from bs4 import BeautifulSoup

from kissmanga.aggregators import Aggregator
from kissmanga.config import KISSMANGA_BASE_PATH, MANGA_NAVIGATION_PARAMS
from kissmanga.helpers import create_dir
from kissmanga.aggregators.chapters import ChapterAggregator


class MangaAggregator(Aggregator):
    async def __init__(
        self,
        navigation_url,
        downloader,
        navigation_params_placeholder=MANGA_NAVIGATION_PARAMS,
    ):
        await super().__init__(navigation_url)
        self.navigation_url = navigation_url
        self.downloader = downloader
        self.navigation_params_placeholder = navigation_params_placeholder
        self.chapters = {}
        # self.path_prefix = path_prefix

    def _scrap_page_content(self):
        chapters = self.soup.find_all(
            lambda tag: "chapter" in tag.attrs.get("href", "")
        )

        def get_chapter_name_and_url(chapter):
            relative_url = chapter.attrs["href"]
            chapter = relative_url.split("/")[-1]
            chapter_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
            return chapter, chapter_url

        # chapter_path_prefix = f"{self.path_prefix}/{chapter}"
        # create_dir(chapter_path_prefix)
        self.chapters = {
            chapter_name: {"chapter_url": chapter_url}
            for chapter_name, chapter_url in list(
                map(get_chapter_name_and_url, chapters)
            )
        }

    async def _retrieve_chapter_pages(self, chapter_name, chapter_url):
        chapter_aggregator = await ChapterAggregator(chapter_url)
        chapter_aggregator.aggregate_content()
        self.chapters[chapter_name]["pages"] = chapter_aggregator.pages

    async def aggregate_content(self):
        self._scrap_page_content()
        await asyncio.gather(
            *[
                self._retrieve_chapter_pages(chapter_name, chapter_value["chapter_url"])
                for chapter_name, chapter_value in self.chapters.items()
            ]
        )