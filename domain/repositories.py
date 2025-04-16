from abc import ABC, abstractmethod
from typing import List
from domain.entities import Product, Property


class ProductRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, uid: str) -> None:
        pass

    @abstractmethod
    async def get_by_uid(self, uid: str) -> Product:
        pass


class PropertyRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Property]:
        pass

    @abstractmethod
    async def create(self, property: Property) -> Property:
        pass

    @abstractmethod
    async def delete(self, uid: str) -> None:
        pass
