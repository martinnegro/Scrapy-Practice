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
from products_by_category.models import RetailCompany, Category, Product


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
            self.retail_company_id = retail_query.id
        else:
            retail_instance = RetailCompany(name = retail_name)
            self.retail_company_id = retail_instance.id
            session.add(retail_instance)
            session.commit()
            session.refresh(retail_instance)
            self.retail_company_id = retail_instance.id

    def process_item(self, item, spider):
        print(f'\n\n===================\n!!!!!self.retail_company_id: {self.retail_company_id}\n=========================\n\n')
        

    def close_spider(self, spider):
        self.Session