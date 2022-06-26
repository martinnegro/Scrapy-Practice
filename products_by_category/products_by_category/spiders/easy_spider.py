import scrapy
from scrapy_selenium import SeleniumRequest
import json
import os
from urllib.parse import urljoin

from scrapy.loader import ItemLoader
from products_by_category.items import ProductItem

class EasySpider(scrapy.Spider):
    name = 'easy'
    categories_file = open(f'{os.path.dirname(__file__)}/paths/easy_categories_path.json')
    categories = json.loads(categories_file.read())
    start_urls = [ 'https://www.easy.com.ar/' + category for category in categories ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)
    
    def parse_category(self, response):
        category_name = response.css('h1.vtex-search-result-3-x-galleryTitle--layout.t-heading-1::text').get()
        products = response.css('article')
        for product in products:
            product_loader = ItemLoader(item=ProductItem(),selector=product)

            product_loader.add_css('product_name','span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-productBrand--shelf-product-name.vtex-product-summary-2-x-brandName.vtex-product-summary-2-x-brandName--shelf-product-name.t-body::text')
            
            price_spans = product.css('span.vtex-product-price-1-x-currencyContainer span::text').getall()
            product_price = ''.join(price_spans).replace('$','').replace('.','').replace(',','.').strip(' ')
            print(f' ====>>>>> PRODUCT_PRICE: {product_price}')
            product_loader.add_value('product_price',product_price)
            
            brand_name = product.css('span.vtex-product-summary-2-x-productBrandName.vtex-product-summary-2-x-productBrandName--shelf-product-brand::text').get()
            print(f' ====>>>>> BRAND_NAME: {brand_name}')
            product_loader.add_value('brand_name',brand_name)
            
            product_loader.add_value('category_name',category_name) 
            
            yield product_loader.load_item()
        
    def parse(self, response):
        anchor_tags = response.css('a.arcencohogareasy-store-theme-5-x-ChildrenCategoriesLink::attr(href)').getall()
        for href in anchor_tags:
            url = urljoin('https://www.easy.com.ar/',href)
            yield SeleniumRequest(url=url,callback=self.parse_category,wait_time=10,)