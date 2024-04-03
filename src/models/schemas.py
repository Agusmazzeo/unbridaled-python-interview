from pydantic import BaseModel
from pydantic import Field

from src.models.product import Product
from src.models.product import ProductVariant


def to_lower_camel(string: str):
    return string.partition("_")[0] + "".join(
        word.capitalize() for word in string.split("_")[1:]
    )


class LowerCamelAlias(BaseModel):
    class Config:
        alias_generator = to_lower_camel
        populate_by_name = True


class AliveResponse(LowerCamelAlias):
    alive: bool


class VariantCreateSchema(LowerCamelAlias, ProductVariant):
    created_at: None = Field(None)
    updated_at: None = Field(None)


class ProductCreateSchema(LowerCamelAlias, Product):
    variants: list[VariantCreateSchema] | None = Field(default_factory=list)
    created_at: None = Field(None)
    updated_at: None = Field(None)


class ProductResponseSchema(LowerCamelAlias, Product):
    pass
