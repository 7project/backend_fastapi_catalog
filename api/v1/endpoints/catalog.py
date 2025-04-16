from fastapi import APIRouter, Depends

from api.dependencies import get_product_service
from api.schemas import ProductSchema
from application.services import ProductService

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/", response_model=list[ProductSchema])
async def list_products(service: ProductService = Depends(get_product_service)):
    return await service.list_products()


@router.post("/", response_model=ProductSchema)
async def create_product(product: ProductSchema,
                         service: ProductService = Depends(get_product_service)):
    return await service.add_product(product)
