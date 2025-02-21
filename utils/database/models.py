from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'scraped_products'
    
    Title = Column(String, primary_key=True)
    Price = Column(Float)
    Rating = Column(Float)
    Colors = Column(Integer)
    Size = Column(String)
    Gender = Column(String)
    timestamp = Column(String)