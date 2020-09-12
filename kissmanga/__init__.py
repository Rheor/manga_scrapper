import requests
from bs4 import BeautifulSoup

class Aggregator():

    def __init__(self, navigation_url):
        raw_content = requests.get(navigation_url).text
        self.soup = BeautifulSoup(raw_content, "html.parser")

    def aggregate_content(self):
        raise NotImplementedError("You should implement an aggregator method.")