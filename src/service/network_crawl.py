import requests
from bs4 import BeautifulSoup


class NetworkCrawl:
    def __init__(self, url):
        self.주소 = url

    def 읽기(self):
        return requests.get(self.주소)
    
    def 크롤링(self):
        return BeautifulSoup(self.읽기().content, 'html.parser')
    
    def 상세크롤링(self):
        return BeautifulSoup(self.읽기().content, 'html.parser')