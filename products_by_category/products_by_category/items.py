# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ProductItem(Item):
    product_name = Field()
    product_price = Field()
    brand_name = Field()
    category_name = Field()