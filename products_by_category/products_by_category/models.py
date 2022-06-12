from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RetailCompany(Base):
    __tablename__ = 'retail_companies'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String, nullable=False)

    categories = relationship('Category',back_populates='retail_company', cascade='all, delete-orphan')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    retail_company_id = Column(UUID, ForeignKey('retail_companies.id'), nullable=False)

    retail_company =  relationship('RetailCompany',back_populates='categories')
    products = relationship('Product',back_populates='category', cascade='all, delete-orphan')

class Product(Base):
    __tablename__ = 'products'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String)
    price = Column(Float)
    category_id = Column(UUID, ForeignKey('categories.id'), nullable=False)

    category = relationship('Category',back_populates='products')