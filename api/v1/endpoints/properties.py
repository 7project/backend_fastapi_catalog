from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_property_service
from api.schemas import PropertySchema
from application.services import PropertyService


router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("/", response_model=list[PropertySchema])
async def list_products(service: PropertyService = Depends(get_property_service)):
    return await service.list_properties()


@router.post("/", response_model=PropertySchema)
async def create_property(property: PropertySchema,
                          service: PropertyService = Depends(get_property_service)):
    return await service.add_property(property)


@router.delete("/{uid}", status_code=204)
async def delete_property(uid: str,
                          service: PropertyService = Depends(get_property_service)):
    deleted = await service.remove_property(uid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return None
