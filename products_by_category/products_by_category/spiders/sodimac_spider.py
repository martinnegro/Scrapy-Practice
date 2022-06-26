import scrapy
from scrapy.loader import ItemLoader
from products_by_category.items import ProductItem

class SodimacSpider(scrapy.Spider):
    name = 'sodimac'
    start_urls = [ 'https://www.sodimac.com.ar/sodimac-ar/' ]

    def parse_category_page(self, response):
        category_name = response.css('h1.jsx-245626150.category-title::text').get()
        if category_name is None: return

        products = response.css('div.jsx-411745769.product.ie11-product-container')
        for product in products:
            product_loader = ItemLoader(item=ProductItem(), selector=product)
            
            product_loader.add_css('product_name','h2.jsx-411745769.product-title::text')

            product_price = product.css('span.jsx-4135487716::text').get().replace('$','').replace('.','')
            product_loader.add_value('product_price',product_price)
            product_loader.add_css('brand_name','div.jsx-411745769.product-brand::text')
            product_loader.add_value('category_name',category_name) 
            
            yield product_loader.load_item()

    def parse(self, response):
        menu = response.css('ul.MenuMobile-module_limited__2f7X-')
        categories = menu.css('a')
        for category in categories:
            category_path = category.css('a::attr(href)').get()
            if category_path is None: continue
            # Checks if link is to a category page
            category_subpath = category_path.split('/')[2]
            if category_subpath == 'category' or category_subpath == 'landing':
                url = 'https://www.sodimac.com.ar' + category_path
                yield scrapy.Request(url,callback=self.parse_category_page) 