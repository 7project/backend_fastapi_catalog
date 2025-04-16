from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PropertyValue:
    value: str
    value_uid: Optional[str]


@dataclass
class Property:
    name: str
    type: str
    uid: Optional[str]
    values: List[PropertyValue]


@dataclass
class Product:
    name: str
    properties: List[Property]
    uid: Optional[str]
