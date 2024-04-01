from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field
from sqlmodel import SQLModel


class ConfigAttribute(BaseModel):
    config_name: str
    config_value: str


class ProductVariant(BaseModel):
    id: int
    sku: str
    sales_price: int
    product_id: int
    purchase_price: int
    type: str
    created_at: str
    updated_at: str
    config_attributes: list[ConfigAttribute]


class Product(BaseModel):
    id: int | None = None
    name: str
    uom: str
    category_name: str
    is_producible: bool
    is_purchasable: bool
    type: str
    purchase_uom: str
    purchase_uom_conversion_rate: int
    batch_tracked: bool
    variants: list[ProductVariant] | None = None
    additional_info: str
    created_at: str
    updated_at: str


# ============= Database Models ============= #


class ProductVariant2ConfigAttributeTable(SQLModel, table=True):
    __tablename__ = "product_variants_to_config_attributes"
    product_variant_id: int | None = Field(
        default=None, foreign_key="product_variant.id", primary_key=True
    )
    config_attribute_id: int | None = Field(
        default=None, foreign_key="config_attribute.id", primary_key=True
    )


class Product2VariantsTable(SQLModel, table=True):
    __tablename__ = "product_to_variants"
    product_id: int | None = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    variant_id: int | None = Field(
        default=None, foreign_key="product_variant.id", primary_key=True
    )


class ConfigAttributeTable(SQLModel, table=True):
    __tablename__ = "config_attribute"
    id: int | None = Field(default=None, primary_key=True)
    config_name: str
    config_value: str


class ProductVariantTableBase(SQLModel, table=True):
    __tablename__ = "product_variant"
    id: int | None = Field(default=None, primary_key=True)
    sku: str
    sales_price: int
    product_id: int
    purchase_price: int
    type: str
    created_at: datetime
    updated_at: datetime


class ProductTableBase(SQLModel, table=True):
    __tablename__ = "product"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    uom: str
    category_name: str
    is_producible: bool
    is_purchasable: bool
    type: str
    purchase_uom: str
    purchase_uom_conversion_rate: int
    batch_tracked: bool
    additional_info: str
    created_at: datetime
    updated_at: datetime


# class ProductVariantTable(ProductVariantTableBase, table=True):
#     __tablename__ = "product_variant"
#     config_attributes: list[ConfigAttributeTable] = Relationship(back_populates="variants", link_model=ProductVariant2ConfigAttributeTable)
#     product: "ProductTable" = Relationship(back_populates="variants", link_model=Product2VariantsTable)

#     class Config:
#         arbitrary_types_allowed = True


# class ProductTable(SQLModel, table=True):
#     __tablename__ = "product"
#     variants: list[ProductVariantTable] = Relationship(back_populates="product", link_model=Product2VariantsTable)

#     class Config:
#         arbitrary_types_allowed = True
