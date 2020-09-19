import copy
import asyncio
import unittest
from unittest.mock import patch, call
from tests.kissmanga.data.mangas_dict import MANGA_DICT
from kissmanga.downloaders.local_downloader import LocalMangaDownloader


ROOT_PATH = "path_bidon"


class TestLocalMangaDownloader(unittest.TestCase):
    def setUp(self):
        self.local_manga_downloader = LocalMangaDownloader(ROOT_PATH)
        self.manga_dict = copy.deepcopy(MANGA_DICT)

    def _assert_chapters_directories_are_built(
        self, manga_name, manga_data, mock_mkdir_calls
    ):
        chapters = manga_data["chapters"]
        for chapter_name, chapter_data in chapters.items():
            assert call(f"{ROOT_PATH}/{manga_name}/{chapter_name}") in mock_mkdir_calls

    @patch("aiofiles.os.mkdir")
    def test_build_tree(self, mock_mkdir):
        asyncio.run(self.local_manga_downloader.build_tree(self.manga_dict))
        file_creation_calls = mock_mkdir.mock_calls

        for manga_name, manga_data in self.manga_dict.items():
            assert call(f"{ROOT_PATH}/{manga_name}") in file_creation_calls
            self._assert_chapters_directories_are_built(
                manga_name, manga_data, file_creation_calls
            )
