import time
import requests
from bs4 import BeautifulSoup

from kissmanga.config import KISSMANGA_BASE_PATH
from kissmanga.helpers import create_dir
from kissmanga.chapters import process_chapter

def process_single_manga(manga_url, path_prefix):
    manga_page_content = requests.get(manga_url).text
    manga_soup = BeautifulSoup(manga_page_content, "html.parser")
    chapters = manga_soup.find_all(lambda tag: "chapter" in tag.attrs.get("href", ""))
    for chapter in chapters:
        relative_url = chapter.attrs["href"]
        chapter = relative_url.split("/")[-1]
        chapter_path_prefix = f"{path_prefix}/{chapter}"
        create_dir(chapter_path_prefix)
        chapter_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
        process_chapter(chapter_url, chapter_path_prefix)
        time.sleep(1)