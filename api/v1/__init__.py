from fastapi import APIRouter
from .endpoints.catalog import router as catalog_router
from .endpoints.products import router as products_router
from .endpoints.properties import router as properties_router


def create_v1_router():
    router = APIRouter(prefix="/v1")
    router.include_router(catalog_router)
    router.include_router(products_router)
    router.include_router(properties_router)
    return router
