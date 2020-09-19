import os
import asyncio
import aiofiles
from kissmanga.exceptions import FolderCreationError


class LocalMangaDownloader:
    def __init__(self, root_path):
        self.root_path = root_path

    @staticmethod
    async def _create_dir(path):
        try:
            aiofiles.os.mkdir(path)
        except OSError as exc:
            if "already exists" not in str(exc):
                raise FolderCreationError()

    async def _build_chapter_and_download_images(
        self, manga_path, chapter_name, chapter_data
    ):
        chapter_path = f"{manga_path}/{chapter_name}"
        await self._create_dir(chapter_path)

    async def _build_manga_and_its_chapters_directories(self, manga_name, manga_data):
        manga_path = f"{self.root_path}/{manga_name}"
        await self._create_dir(manga_path)

        async_chapter_creations = [
            self._build_chapter_and_download_images(
                manga_path, chapter_name, chapter_data
            )
            for chapter_name, chapter_data in manga_data["chapters"].items()
        ]
        await asyncio.gather(*async_chapter_creations)

    async def _build_mangas_directories(self, manga_dict):
        async_dir_creations = [
            self._build_manga_and_its_chapters_directories(manga_name, manga_data)
            for manga_name, manga_data in manga_dict.items()
        ]
        await asyncio.gather(*async_dir_creations)

    async def build_tree(self, mangas_dict):
        await self._build_mangas_directories(mangas_dict)