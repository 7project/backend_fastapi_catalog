from domain.entities import Product as DomainProduct, Property as DomainProperty, PropertyValue as DomainPropertyValue
from infrastructure.db.models import Product as DBProduct, Property as DBProperty, PropertyValue as DBPropertyValue
from fastapi import HTTPException


async def db_to_domain_product(db_product: DBProduct) -> DomainProduct:
    print("Loading properties...")
    properties = await db_product.awaitable_attrs.properties
    print(f"Properties loaded: {len(properties)}")

    return DomainProduct(
        uid=db_product.uid,
        name=db_product.name,
        properties=[
            DomainProperty(
                uid=p.uid,
                name=p.name,
                type=p.type,
                values=[
                    DomainPropertyValue(value_uid=v.value_uid, value=v.value)
                    for v in p.values
                ]
            )
            for p in db_product.properties
        ]
    )


async def db_to_domain_property(db_property: DBProperty) -> DomainProperty:
    return DomainProperty(
        uid=db_property.uid,
        name=db_property.name,
        type=db_property.type,
        values=[
            DomainPropertyValue(value_uid=v.value_uid, value=v.value)
            for v in db_property.values
        ]
    )


async def domain_to_db_product(domain_product: DomainProduct) -> DBProduct:
    return DBProduct(
        uid=domain_product.uid,
        name=domain_product.name,
        properties=[
            DBProperty(
                uid=p.uid,
                name=p.name,
                type=p.type,
                product_uid=domain_product.uid,
                values=[
                    DBPropertyValue(value_uid=v.value_uid, value=v.value)
                    for v in p.values
                ]
            )
            for p in domain_product.properties
        ]
    )


async def domain_to_db_property(domain_property: DomainProperty) -> DBProperty:
    return DBProperty(
        uid=domain_property.uid,
        name=domain_property.name,
        type=domain_property.type,
        values=[
            DBPropertyValue(value_uid=v.value_uid, value=v.value)
            for v in domain_property.values
        ]
    )
