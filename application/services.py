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
