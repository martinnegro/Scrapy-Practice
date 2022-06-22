import scrapy
from scrapy_selenium import SeleniumRequest
import json
import os
from urllib.parse import urljoin

class EasySpider(scrapy.Spider):
    name = 'easy'
    categories_file = open(f'{os.path.dirname(__file__)}/paths/easy_categories_path.json')
    categories = json.loads(categories_file.read())
    start_urls = [ 'https://www.easy.com.ar/' + category for category in categories ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)
    
    def parse_category(self, response):
        title =  response.css('h1.vtex-search-result-3-x-galleryTitle--layout.t-heading-1::text').get()
        print(f' ===>>> response: {title}')
        
    def parse(self, response):
        anchor_tags = response.css('a.arcencohogareasy-store-theme-5-x-ChildrenCategoriesLink::attr(href)').getall()
        for href in anchor_tags:
            url = urljoin('https://www.easy.com.ar/',href)
            print(f' ===>>> response: {url}')
            yield SeleniumRequest(url=url,callback=self.parse_category,wait_time=10)