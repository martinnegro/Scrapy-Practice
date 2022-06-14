from enum import unique
import uuid
from click import echo
from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy import Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get('DB_URI'),echo=True,future=True)

def create_tables(engine):
    Base.metadata.create_all(engine)

class RetailCompany(Base):
    __tablename__ = 'retail_companies'
        
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String, nullable=False,unique=True)

    categories = relationship('Category',back_populates='retail_company', cascade='all, delete-orphan')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    retail_company_id = Column(UUID(as_uuid=True), ForeignKey('retail_companies.id'), nullable=False)

    retail_company =  relationship('RetailCompany',back_populates='categories')
    products = relationship('Product',back_populates='category', cascade='all, delete-orphan')

class Brand(Base):
    __tablename__ = 'brands'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String, nullable=False,unique=True)

    products = relationship('Product',back_populates='brand', cascade='all, delete-orphan')

class Product(Base):
    __tablename__ = 'products'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String)
    price = Column(Float)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    brand_id =  Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)

    category = relationship('Category',back_populates='products')
    brand = relationship('Brand',back_populates='products')