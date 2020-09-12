import requests
from kissmanga import Aggregator
from bs4 import BeautifulSoup

class ChapterAggregator(Aggregator):
    
    def __init__(self, navigation_url, path_prefix):
        super().__init__(navigation_url)
        self.navigation_url = navigation_url
        self.path_prefix = path_prefix

    def _scrap_page_content(self):
        chapter_images = [
            chapter_image
            for chapter_image in list(self.soup.find(id="centerDivVideo").children)
            if chapter_image != "\n" and getattr(chapter_image, "name") == "img"
        ]
        
        for index, image in enumerate(chapter_images):
            image_url = image.attrs.get("src")
            image_extension = image_url.split(".")[-1]
            image_raw = requests.get(image_url).content
            image_path = f"{self.path_prefix}/{index}.{image_extension}"
            with open(image_path, "wb+") as f:
                f.write(image_raw)

    def aggregate_content(self):
        self._scrap_page_content()