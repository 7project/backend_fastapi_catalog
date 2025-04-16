from fastapi import Depends
from infrastructure.db.database import get_db
from application.services import ProductService, PropertyService
from infrastructure.db.repositories import SQLProductRepository, SQLPropertyRepository


async def get_product_service(db=Depends(get_db)):
    return ProductService(SQLProductRepository(db))


async def get_property_service(db=Depends(get_db)):
    return PropertyService(SQLPropertyRepository(db))
