import scrapy

class SodimacSpider(scrapy.Spider):
    import scrapy
# from scrapy_splash import SplashRequest

class SodimacSpider(scrapy.Spider):
    name = 'sodimac'
    start_urls = [ 'https://www.sodimac.com.ar/sodimac-ar/' ]

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse_page_category(self,response):
        items = response.css('div.jsx-411745769.product.ie11-product-container')
        products = [
                    {
                        'brand_name': item.css('div.jsx-411745769.product-brand::text').get(),
                        'product_name': item.css('h2.jsx-411745769.product-title::text').get(),
                        'product_price': item.css('div.jsx-4135487716.price.jsx-175035124 span::text').get()
                    } for item in items
        ]
        yield {
            'category_name': response.css('h1.jsx-245626150.category-title::text').get(),
            'category_products': products
        }

    def parse(self, response):
        menu = response.css('ul.MenuMobile-module_limited__2f7X-')
        categories = menu.css('a')
        for category in categories:
            category_page = category.css('a::attr(href)').get()
            if category_page:
                yield scrapy.Request('https://www.sodimac.com.ar' + category_page,callback=self.parse_page_category)