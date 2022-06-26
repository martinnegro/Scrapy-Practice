# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter


from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert
from products_by_category.models import create_tables, db_connect
from products_by_category.models import RetailCompany, Category, Product, Brand


class JsonLPipeline:
    def open_spider(self, spider):
        spider_name = spider.name
        self.file = open(f'{spider_name}.jl','w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(adapter.asdict()) + "\n"
        self.file.write(line)

        return item

class DBPipeline:
    brand_ids = {}
    category_ids = {}

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        # Here we find or create the retail_company_id
        # so it's available for make relationships
        session = self.Session()
        retail_name =  spider.name

        retail_query = select(RetailCompany).where(RetailCompany.name == retail_name)
        retail_result = session.execute(retail_query).fetchone()

        if retail_result is not None:
            self.retail_company_id = retail_result[0].id
        else:
            retail_instance = RetailCompany(name = retail_name)
            session.add(retail_instance)
            session.commit()
            session.refresh(retail_instance)
            self.retail_company_id = retail_instance.id
        
        session.close()

    def process_item(self, item, spider):
        ### Process brand
        session = self.Session()
        
        brand_name = item['brand_name'][0]
        brand_id = None
        
        if brand_name in self.brand_ids:
            brand_id = self.brand_ids[brand_name]
        else:
            brand_query = select(Brand).where(Brand.name == brand_name)
            brand_result = session.execute(brand_query).fetchone()
            if brand_result is not None:
                brand_id = brand_result[0].id
                self.brand_ids[brand_name] = brand_result[0].id
            else:
                brand_instance = Brand(name = brand_name)
                session.add(brand_instance)
                session.commit()
                session.refresh(brand_instance)
                brand_id = brand_instance.id
                self.brand_ids[brand_name] = brand_instance.id

        ### Process category
        category_name = item['category_name'][0]
        category_id = None

        if category_name in self.category_ids:
            category_id = self.category_ids[category_name]
        else:
            # Check for category relationed with retail
            category_query = select(Category).where(Category.name == category_name,Category.retail_company_id == self.retail_company_id)
            category_result = session.execute(category_query).fetchone()
            if category_result is not None:
                category_id = category_result[0].id
                self.category_ids[category_name] = category_result[0].id
            else:
                category_instance = Category(name = category_name,retail_company_id=self.retail_company_id)
                session.add(category_instance)
                session.commit()
                session.refresh(category_instance)
                category_id = category_instance.id
                self.category_ids[category_name] = category_instance.id
        
        product_price = item['product_price'][0]
        product_instance = Product(
            name = item['product_name'][0],
            price = product_price,
            category_id = category_id,
            brand_id = brand_id
        )
        session.add(product_instance)
        session.commit()

        session.close()

    def close_spider(self, spider):
        pass