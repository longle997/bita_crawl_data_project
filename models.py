from sqlalchemy import Column, Integer, String

from database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    sale_price = Column(String)
    sold_number = Column(String)
    original_price = Column(String)
    sale_percentage = Column(String)
    sold_number = Column(String)
    review_number = Column(String)
    vendor_location = Column(String)
