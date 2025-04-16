from typing import Dict, Optional

from fastapi import HTTPException
from domain.repositories import ProductRepository, PropertyRepository
from domain.entities import Product, Property, PropertyValue
from application.dto import ProductDTO, PropertyDTO, PropertyValueDTO, ProductResponseDTO


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def list_products(self) -> list[ProductDTO]:
        products = await self.repository.get_all()
        return [ProductDTO(
            uid=p.uid,
            name=p.name,
            properties=[PropertyDTO(
                uid=prop.uid,
                name=prop.name,
                type=prop.type,
                values=[PropertyValueDTO(value_uid=v.value_uid, value=v.value) for v in prop.values]
            ) for prop in p.properties]
        ) for p in products]

    async def add_product(self, product_dto: ProductDTO) -> ProductDTO:
        domain_product = Product(
            uid=None,
            name=product_dto.name,
            properties=[Property(
                uid=None,
                name=p.name,
                type=p.type,
                values=[PropertyValue(value_uid=None, value=v.value) for v in p.values]
            ) for p in product_dto.properties]
        )
        created_product = await self.repository.create(domain_product)
        return ProductDTO(
            uid=created_product.uid,
            name=created_product.name,
            properties=[PropertyDTO(
                uid=prop.uid,
                name=prop.name,
                type=prop.type,
                values=[PropertyValueDTO(value_uid=v.value_uid, value=v.value) for v in prop.values]
            ) for prop in created_product.properties]
        )

    async def get_product(self, uid: str) -> ProductResponseDTO:
        # Получаем товар из репозитория с загрузкой связанных данных
        db_product = await self.repository.get_by_uid(uid)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Преобразуем ORM-модель в DTO
        return ProductResponseDTO(
            uid=db_product.uid,
            name=db_product.name,
            properties=[
                {
                    "uid": p.uid,
                    "name": p.name,
                    "type": p.type,
                    "values": [
                        {"value_uid": v.value_uid, "value": v.value}
                        for v in p.values
                    ]
                }
                for p in db_product.properties
            ]
        )

    async def delete_product(self, uid: str) -> bool:
        await self.repository.delete(uid)
        return True

    async def catalog_list_products(
        self,
        page: int = 1,
        page_size: int = 10,
        filters:  list[str] | None = None,
        name: str | None = None,
        sort: str = "uid",
    ) -> dict:

        parsed_filters = {}
        if filters:
            for filter_str in filters:
                key, value = filter_str.split(":", 1)
                if key not in parsed_filters:
                    parsed_filters[key] = []
                parsed_filters[key].append(value)

        result = await self.repository.get_filtered_products(page, page_size, parsed_filters, name, sort)
        return {
            "products": [
                ProductDTO(
                    uid=p.uid,
                    name=p.name,
                    properties=[
                        PropertyDTO(
                            uid=prop.uid,
                            name=prop.name,
                            type=prop.type,
                            values=[PropertyValueDTO(value_uid=v.value_uid, value=v.value) for v in prop.values]
                        )
                        for prop in p.properties
                    ]
                )
                for p in result["products"]
            ],
            "count": result["count"],
        }

    async def get_filter_statistics(
        self,
        filters: list[str] | None = None,
        name: str | None = None,
    ) -> dict:
        parsed_filters = {}
        if filters:
            for filter_str in filters:
                key, value = filter_str.split(":", 1)
                if key not in parsed_filters:
                    parsed_filters[key] = []
                parsed_filters[key].append(value)

        filtered_products = await self.repository.get_filtered_products(filters=parsed_filters, name=name)

        property_stats = {}
        for product in filtered_products["products"]:
            for prop in product.properties:
                if prop.uid not in property_stats:
                    property_stats[prop.uid] = {}

                if prop.type == "int":

                    values = [int(v.value) for v in prop.values]
                    property_stats[prop.uid]["min_value"] = min(property_stats[prop.uid].get("min_value", float("inf")), min(values))
                    property_stats[prop.uid]["max_value"] = max(property_stats[prop.uid].get("max_value", float("-inf")), max(values))
                else:

                    for value in prop.values:
                        property_stats[prop.uid][value.value] = property_stats[prop.uid].get(value.value, 0) + 1

        return {
            "count": filtered_products["count"],
            **property_stats,
        }


class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    async def list_properties(self) -> list[PropertyDTO]:
        properties = await self.repository.get_all()
        return [PropertyDTO(
            uid=p.uid,
            name=p.name,
            type=p.type,
            values=[PropertyValueDTO(value_uid=v.value_uid, value=v.value) for v in p.values]
        ) for p in properties]

    async def add_property(self, property_dto: PropertyDTO) -> PropertyDTO:
        domain_property = Property(
            uid=property_dto.uid,
            name=property_dto.name,
            type=property_dto.type,
            values=[PropertyValue(value_uid=v.value_uid, value=v.value) for v in property_dto.values]
        )
        created_property = await self.repository.create(domain_property)
        return PropertyDTO(
            uid=created_property.uid,
            name=created_property.name,
            type=created_property.type,
            values=[PropertyValueDTO(value_uid=v.value_uid, value=v.value) for v in created_property.values]
        )

    async def remove_property(self, uid: str) -> bool:
        await self.repository.delete(uid)
        return True
