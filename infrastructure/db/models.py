from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from infrastructure.db.database import Base
from uuid import uuid4


class ProductPropertyAssociation(Base):
    __tablename__ = "product_property"

    product_uid: Mapped[str] = mapped_column(
        String, ForeignKey("products.uid"), primary_key=True
    )
    property_uid: Mapped[str] = mapped_column(
        String, ForeignKey("properties.uid"), primary_key=True
    )


class Product(Base):
    __tablename__ = "products"

    uid: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)

    properties: Mapped[List["Property"]] = relationship(
        "Property", back_populates="products", secondary="product_property",
        lazy="selectin",
        cascade="save-update",
    )


class Property(Base):
    __tablename__ = "properties"

    uid: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

    products: Mapped[List["Product"]] = relationship("Product",
                                                     back_populates="properties",
                                                     secondary="product_property",
                                                     cascade="save-update")

    values: Mapped[List["PropertyValue"]] = relationship(
        "PropertyValue",
        back_populates="property",
        lazy="selectin",
        cascade="all, delete",
    )


class PropertyValue(Base):
    __tablename__ = "property_values"

    value_uid: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    value: Mapped[str] = mapped_column(String, nullable=False)
    property_uid: Mapped[str] = mapped_column(ForeignKey("properties.uid"), nullable=False)

    property: Mapped["Property"] = relationship("Property", back_populates="values")
