from fastapi import FastAPI
from api.v1 import create_v1_router
from infrastructure.db.database import get_db
from application.services import ProductService, PropertyService
from api.dependencies import get_product_service, get_property_service


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="Catalog API", version="1.0.0")

    app.include_router(create_v1_router())

    @app.get("/")
    async def index():
        return {"message": "Catalog API is start!"}

    return app
