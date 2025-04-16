from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyValueDTO(BaseModel):
    value_uid: Optional[str] = None
    value: str


class PropertyDTO(BaseModel):
    uid: Optional[str] = None
    name: str
    type: str
    values: List[PropertyValueDTO] = None


class ProductDTO(BaseModel):
    uid: Optional[str] = None
    name: str
    properties: Optional[List[PropertyDTO]] = None


class ProductResponseDTO(BaseModel):
    uid: Optional[str] = None
    name: str
    properties: List[PropertyDTO]


class CatalogResponse(BaseModel):
    products: List[ProductDTO]
    count: int
