from typing import List, Dict, Optional
from uuid import uuid4

from sqlalchemy.future import select
from sqlalchemy import func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from domain.repositories import ProductRepository
from infrastructure.db.models import Product as DBProduct, Property as DBProperty, PropertyValue as DBPropertyValue, \
    ProductPropertyAssociation
from infrastructure.db.mappings import db_to_domain_product, domain_to_db_product
from domain.entities import Property as DomainProperty
from domain.entities import Product as DomainProduct
from domain.repositories import PropertyRepository
from infrastructure.db.mappings import db_to_domain_property, domain_to_db_property
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert
from fastapi import HTTPException


class SQLProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[DomainProduct]:
        stmt = select(DBProduct).options(
            selectinload(DBProduct.properties).selectinload(DBProperty.values))
        result = await self.session.execute(stmt)
        db_products = result.scalars().all()
        return [await db_to_domain_product(p) for p in db_products]

    async def create(self, product: DomainProduct) -> DomainProduct:

        try:

            if product.uid is None:
                product.uid = str(uuid4())

            db_product = await self.session.get(
                DBProduct,
                product.uid,
                options=[selectinload(DBProduct.properties)],
            )
            try:
                if db_product is None:
                    db_product = DBProduct(uid=product.uid, name=product.name)
                    self.session.add(db_product)
                    await self.session.flush()

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"LOCAL ->>>> Error creating product: {e}",
                )
            for property in product.properties:
                db_property = await self.session.get(DBProperty, property.uid)
                if db_property is None:

                    db_property = DBProperty(
                        uid=str(uuid4()) if property.uid is None else property.uid,
                        name=property.name,
                        type=property.type,
                    )
                    self.session.add(db_property)
                    await self.session.flush()

                await self.session.execute(
                    insert(ProductPropertyAssociation)
                    .values(
                        product_uid=db_product.uid,
                        property_uid=db_property.uid,
                    )
                    .on_conflict_do_nothing()
                )

                try:
                    for value in property.values:
                        stmt = (
                            select(DBPropertyValue)
                            .where(
                                DBPropertyValue.property_uid == db_property.uid,
                                DBPropertyValue.value_uid == value.value_uid,
                            )
                        )
                        db_value = (await self.session.execute(stmt)).scalars().one_or_none()

                        if db_value is None:
                            db_value = DBPropertyValue(
                                value_uid=str(uuid4()) if value.value_uid is None else value.value_uid,
                                value=value.value,
                                property_uid=db_property.uid,
                            )
                            self.session.add(db_value)

                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"LOCAL ->>>> Error creating property: {e}",
                    )

            try:
                await self.session.commit()
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"LOCAL ->>>> Error creating product: {e}",
                )

            try:

                stmt = (select(DBProduct).options(
                    selectinload(DBProduct.properties).selectinload(DBProperty.values))
                        .where(DBProduct.uid == product.uid))
                result = await self.session.execute(stmt)
                db_product = result.scalar_one_or_none()

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"LOCAL ->>>> Error await self.session.get: {e}",
                )

            if db_product is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Product with UID {product.uid} was not found after creation.",
                )

            try:

                result = await db_to_domain_product(db_product)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"LOCAL ->>>> Error db_to_domain_product: {e}",
                )

            return result

        except Exception as e:
            print(f"BASE >>>>> Error during product creation: {e}")
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while creating the product.")

    async def get_by_uid(self, uid: str) -> DomainProduct:
        stmt = select(DBProduct).options(selectinload(DBProduct.properties)).where(DBProduct.uid == uid)
        result = await self.session.execute(stmt)
        db_product = result.scalar_one_or_none()
        if not db_product:
            raise HTTPException(status_code=404, detail=f"Product with UID {uid} not found")
        return await db_to_domain_product(db_product)

    async def delete(self, uid: str) -> bool:
        stmt = select(DBProduct).where(DBProduct.uid == uid)
        result = await self.session.execute(stmt)
        db_product = result.scalar_one_or_none()
        if not db_product:
            return False
        await self.session.delete(db_product)
        await self.session.commit()
        return True

    async def get_filtered_products(
            self,
            page: int = 1,
            page_size: int = 10,
            filters: Optional[Dict[str, List[str]]] = None,
            name: Optional[str] = None,
            sort: str = "uid",
    ) -> dict:
        stmt = select(DBProduct).options(
            selectinload(DBProduct.properties).selectinload(DBProperty.values)
        )

        if name:
            stmt = stmt.where(DBProduct.name.ilike(f"%{name}%"))

        if filters:
            filter_conditions = []
            for prop_uid, values in filters.items():
                if isinstance(values, dict) and "from" in values and "to" in values:
                    filter_conditions.append(
                        and_(
                            DBProperty.uid == prop_uid,
                            DBPropertyValue.value.between(values["from"], values["to"]),
                        )
                    )
                else:
                    filter_conditions.append(
                        and_(
                            DBProperty.uid == prop_uid,
                            DBPropertyValue.value.in_(values),
                        )
                    )
            stmt = stmt.join(DBProduct.properties).join(DBProperty.values).where(or_(*filter_conditions))

        if sort == "name":
            stmt = stmt.order_by(DBProduct.name.asc())
        else:
            stmt = stmt.order_by(DBProduct.uid.asc())

        total_count = await self.session.execute(select(func.count()).select_from(stmt.subquery()))
        total_count = total_count.scalar_one()

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(stmt)
        db_products = result.unique().scalars().all()

        return {
            "products": [await db_to_domain_product(p) for p in db_products],
            "count": total_count,
        }

    async def get_filter_statistics(
            self,
            filters: Optional[Dict[str, List[str]]] = None,
            name: Optional[str] = None,
    ) -> dict:

        filtered_products = await self.get_filtered_products(filters=filters, name=name)

        property_stats = {}
        for product in filtered_products["products"]:
            for prop in product.properties:
                if prop.uid not in property_stats:
                    property_stats[prop.uid] = {}

                if prop.type == "int":
                    values = [int(v.value) for v in prop.values]
                    property_stats[prop.uid]["min_value"] = min(
                        property_stats[prop.uid].get("min_value", float("inf")), min(values)
                    )
                    property_stats[prop.uid]["max_value"] = max(
                        property_stats[prop.uid].get("max_value", float("-inf")), max(values)
                    )
                else:
                    for value in prop.values:
                        property_stats[prop.uid][value.value] = (
                                property_stats[prop.uid].get(value.value, 0) + 1
                        )

        return {
            "count": filtered_products["count"],
            **property_stats,
        }


class SQLPropertyRepository(PropertyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[DomainProperty]:
        stmt = select(DBProperty).options(selectinload(DBProperty.values))
        result = await self.session.execute(stmt)
        db_properties = result.scalars().all()
        return [await db_to_domain_property(p) for p in db_properties]

    async def create(self, property: DomainProperty) -> DomainProperty:
        db_property = await domain_to_db_property(property)
        self.session.add(db_property)
        await self.session.commit()
        await self.session.refresh(db_property)
        return await db_to_domain_property(db_property)

    async def delete(self, uid: str) -> bool:
        stmt = select(DBProperty).where(DBProperty.uid == uid)
        result = await self.session.execute(stmt)
        db_property = result.scalar_one_or_none()
        if not db_property:
            return False
        await self.session.delete(db_property)
        await self.session.commit()
        return True

    async def get_by_uid(self, uid: str) -> DomainProperty:
        stmt = select(DBProperty).options(selectinload(DBProperty.values)).where(DBProperty.uid == uid)
        result = await self.session.execute(stmt)
        db_property = result.scalar_one_or_none()
        if not db_property:
            raise HTTPException(status_code=404, detail=f"Property with UID {uid} not found")
        return await db_to_domain_property(db_property)
