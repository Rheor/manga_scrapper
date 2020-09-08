import requests
from bs4 import BeautifulSoup

def process_chapter(chapter_url, path_prefix):
    chapter_page_content = requests.get(chapter_url).text
    chapter_soup = BeautifulSoup(chapter_page_content)
    chapter_images = [
        chapter_image
        for chapter_image in list(chapter_soup.find(id="centerDivVideo").children)
        if chapter_image != "\n" and getattr(chapter_image, "name") == "img"
    ]
    for index, image in enumerate(chapter_images):
        image_url = image.attrs.get("src")
        image_extension = image_url.split(".")[-1]
        image_raw = requests.get(image_url).content
        image_path = f"{path_prefix}/{index}.{image_extension}"
        with open(image_path, "wb+") as f:
            f.write(image_raw)