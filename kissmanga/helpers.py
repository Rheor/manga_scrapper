import os
import asyncio

from kissmanga.exceptions import FolderCreationError


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if "already exists" not in str(exc):
            raise FolderCreationError()


async def make_request(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.text()