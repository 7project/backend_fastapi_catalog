from fastapi import FastAPI
from api.v1 import create_v1_router


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="Catalog API", version="1.0.0")

    app.include_router(create_v1_router())

    @app.get("/")
    async def index():
        return {"message": "Catalog API is start!"}

    return app
