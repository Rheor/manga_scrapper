import os
import asyncio

from kissmanga.exceptions import FolderCreationError


async def make_request(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.text()