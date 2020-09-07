import os
import time

import requests
from bs4 import BeautifulSoup
LIBRARY_PATH = "library"

DELAY = "10"
KISSMANGA_BASE_PATH = "https://kissmanga.org"
KISSMANGA_LIST_URL = f"{KISSMANGA_BASE_PATH}/manga_list"

class FolderCreationError(Exception):
    pass


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if "already exists" not in str(exc):
            raise FolderCreationError()

def process_chapter(chapter_url, path_prefix):
    chapter_page_content = requests.get(chapter_url).text
    chapter_soup = BeautifulSoup(chapter_page_content)
    chapter_images = [
        chapter_image 
        for chapter_image in list(chapter_soup.find(id="centerDivVideo").children)
        if chapter_image != "\n" and "img" in chapter_image
    ]
    for index, image in enumerate(chapter_images):
        image_url = image.attrs.get("src")
        image_extension = image_url.split(".")[-1]
        image_raw = requests.get(image_url).content
        image_path = f"{path_prefix}/{index}.{image_extension}"
        with open(image_path, "wb+") as f:
            f.write(image_raw)

def process_single_manga(manga_url, path_prefix):
    manga_page_content = requests.get(manga_url).text
    manga_soup = BeautifulSoup(manga_page_content)
    chapters = manga_soup.find_all(
        lambda tag: "chapter" in tag.attrs.get("href", "")
    )
    for chapter in chapters:
        relative_url = chapter.attrs["href"]
        chapter = relative_url.split("/")[-1]
        chapter_path_prefix = f"{path_prefix}/{chapter}"
        create_dir(chapter_path_prefix)
        chapter_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
        process_chapter(chapter_url, chapter_path_prefix)
        time.sleep(1)
    exit(0)

def main():
    url_content = requests.get(KISSMANGA_LIST_URL).text
    soup = BeautifulSoup(url_content)
    mangas_links = soup.find_all(
        name="a", attrs={"class": "item_movies_link"}
    )
    
    for manga_link in mangas_links:
        relative_url = manga_link.get("href")
        manga_name = manga_link.text.replace(" ", "_")
        manga_url = f"{KISSMANGA_BASE_PATH}{relative_url}"
        path_prefix = f"{LIBRARY_PATH}/{manga_name}"
        create_dir(path_prefix)
        process_single_manga(manga_url, path_prefix)

if __name__ == "__main__":
    main()