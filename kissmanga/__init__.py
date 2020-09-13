import aiohttp

from bs4 import BeautifulSoup
from kissmanga.helpers import make_request


class Aggregator:
    async def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        await instance.__init__(*args, **kwargs)
        return instance

    async def __init__(self, navigation_url):
        async with aiohttp.ClientSession() as session:
            raw_content = await make_request(session, navigation_url)
            self.soup = BeautifulSoup(raw_content, "html.parser")

    def aggregate_content(self):
        raise NotImplementedError("You should implement an aggregator method.")