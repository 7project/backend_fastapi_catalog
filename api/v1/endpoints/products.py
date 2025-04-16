from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_product_service
from api.schemas import ProductSchema, ProductResponseSchema
from application.services import ProductService


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductSchema])
async def list_products(service: ProductService = Depends(get_product_service)):
    return await service.list_products()


@router.post("/", response_model=ProductSchema)
async def create_product(product: ProductSchema,
                         service: ProductService = Depends(get_product_service)):
    return await service.add_product(product)


@router.get("/product/{uid}", response_model=ProductResponseSchema)
async def get_product(
    uid: str,
    service: ProductService = Depends(get_product_service),
):
    product = await service.get_product(uid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/product/{uid}", status_code=204)
async def delete_product(
    uid: str,
    service: ProductService = Depends(get_product_service),
):
    deleted = await service.delete_product(uid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
