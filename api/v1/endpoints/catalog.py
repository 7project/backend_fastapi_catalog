from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, Query

from api.dependencies import get_product_service
from api.schemas import ProductSchema
from application.dto import CatalogResponse
from application.services import ProductService

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/", response_model=CatalogResponse)
async def list_catalog(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    filters: list[str] | None = Query(None),
    name: str | None = Query(None),
    sort: str = Query("uid", regex="^(name|uid)$"),
    service: ProductService = Depends(get_product_service),
):
    return await service.catalog_list_products(page, page_size, filters, name, sort)


@router.get("/filter/", response_model=dict)
async def filter_catalog(
    filters: list[str] | None = Query(None),
    name: str | None = Query(None),
    service: ProductService = Depends(get_product_service),
):
    return await service.get_filter_statistics(filters, name)

