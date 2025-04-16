from abc import ABC, abstractmethod
from typing import List, Dict, Optional
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

    @abstractmethod
    async def get_filtered_products(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, List[str]]] = None,
        name: Optional[str] = None,
        sort: str = "uid",
    ) -> dict:
        pass

    @abstractmethod
    async def get_filter_statistics(
        self,
        filters: Optional[Dict[str, List[str]]] = None,
        name: Optional[str] = None,
    ) -> dict:
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
