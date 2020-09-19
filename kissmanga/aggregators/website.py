import json
import random
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from kissmanga.config import (
    LIBRARY_PATH,
    DELAY,
    KISSMANGA_BASE_PATH,
    KISSMANGA_LIST_URL,
    MANGA_NAVIGATION_PARAMS,
)
from kissmanga.aggregators import Aggregator
from kissmanga.helpers import make_request
from kissmanga.exceptions import FailedAsyncHttpRequest
from kissmanga.aggregators.aggregators import MangaAggregator


class KissmangaAggregator(Aggregator):
    async def __init__(
        self,
        navigation_url,
        semaphore,
        downloader,
        navigation_params_placeholder=MANGA_NAVIGATION_PARAMS,
    ):
        self.page_num = 0
        self.navigation_params_placeholder = navigation_params_placeholder
        self.navigation_url = navigation_url
        self.semaphore = semaphore
        self.downloader = downloader()
        await super().__init__(self._get_page_url())
        self.last_page = self._get_last_page()
        self.mangas = {}

    def _get_page_url(self):
        page_params = self.navigation_params_placeholder.format(self.page_num)
        return f"{self.navigation_url}{page_params}"

    def _get_last_page(self):
        # print(self.navigation_url)
        # last_url = self.soup.find_all("ul")[-1]
        # last_page_link = [
        #     tag
        #     for tag in list(last_url.children)
        #     if tag != "\n" and "Last" in getattr(tag, "text")
        # ][0]
        # last_page = int(last_page_link.text.replace("Last (", "").replace(") ", ""))
        # return last_page
        return 1

    def _scrap_page_content(self):
        mangas_links = self.soup.find_all(name="a", attrs={"class": "item_movies_link"})

        # for manga_link in mangas_links:
        def get_manga_name_and_url(manga_link):
            relative_url = manga_link.get("href")
            manga_name = "".join(char for char in manga_link.text if char.isalnum())
            manga_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
            return manga_name, manga_url

        # path_prefix = f"{LIBRARY_PATH}/{manga_name}"
        # create_dir(path_prefix)
        # MangaAggregator(manga_url, path_prefix).aggregate_content()
        self.mangas = {
            manga_name: {"manga_url": manga_url}
            for manga_name, manga_url in list(map(get_manga_name_and_url, mangas_links))
        }

    async def _paginate(self):
        self.page_num += 1

        async with aiohttp.ClientSession() as session:
            raw_content = await make_request(session, self._get_page_url())

        self.soup = BeautifulSoup(raw_content, "html.parser")
        return self.page_num <= self.last_page

    async def _retrieve_manga_chapters(self, manga_name, manga_url):
        async with self.semaphore:
            print(f"Retrieving data for manga {manga_name}")
            try:
                manga_aggregator = await MangaAggregator(manga_url)
                await manga_aggregator.aggregate_content()
                self.mangas[manga_name]["chapters"] = manga_aggregator.chapters
            except FailedAsyncHttpRequest:
                # This occurs when a chapter content cannot be retrieved
                # as a rule of thumb we consider the manga retrieval failed
                # Who would want a missing chapter in the middle of reading ? :)
                print(f"Failed to retrieve data for manga {manga_name}")

    async def aggregate_content(self):
        while await self._paginate():
            print("paginating")
            print(self.page_num)
            self._scrap_page_content()

        await asyncio.gather(
            *[
                self._retrieve_manga_chapters(manga_name, manga_value["manga_url"])
                for manga_name, manga_value in self.mangas.items()
            ]
        )

        await self.downloader.build_tree(self.mangas)


async def kissmanga(semaphore, downloader):
    kissmanga = await KissmangaAggregator(KISSMANGA_LIST_URL, semaphore, downloader)
    await kissmanga.aggregate_content()
