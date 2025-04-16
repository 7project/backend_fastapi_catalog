from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyValueSchema(BaseModel):
    value_uid: Optional[str] = None
    value: str


class PropertySchema(BaseModel):
    uid: Optional[str] = None
    name: str
    type: str
    values: Optional[List[PropertyValueSchema]] = None


class ProductSchema(BaseModel):
    uid: Optional[str] = None
    name: str
    properties: Optional[List[PropertySchema]] = None


class ProductResponseSchema(BaseModel):
    uid: str
    name: str
    properties: Optional[List[PropertySchema]]
