from src.clients.postgres_client import PostgresClient
from src.models.product import ConfigAttributeTable
from src.models.product import Product
from src.models.product import ProductTableBase
from src.models.product import ProductVariant
from src.models.product import ProductVariantTableBase


class ProductHandler:
    def __init__(self, db_client: PostgresClient) -> None:
        self.db_client = db_client

    def get_all_products_with_variatiants(self) -> list[Product]:
        product_dict: dict[int, Product] = {}
        result = self.db_client.get_all_products_with_variations()
        for product, variant in result:
            if product.id is not None:
                if not product_dict.get(product.id):
                    product_dict[product.id] = Product.model_validate(
                        product.model_dump()
                    )
                if (
                    variant is not None
                    and product_dict[product.id].variants is not None
                ):
                    product_dict[product.id].variants.append(
                        ProductVariant.model_validate(variant.model_dump())
                    )
        return product_dict.values()

    def get_product_by_id(self, product_id: int) -> Product | None:
        product: Product | None = None
        result = self.db_client.get_product_by_id(product_id)
        for p, variant in result:
            if product is None:
                product = Product.model_validate(p.model_dump())
            if variant is not None:
                product.variants.append(
                    ProductVariant.model_validate(variant.model_dump())
                )
        return product

    def create_product(self, product: Product) -> Product:
        created_product = self.db_client.create_product(
            product=ProductTableBase.model_validate(
                product.model_dump(exclude_none=True)
            )
        )
        product.id = created_product.id

        for variant in product.variants:
            created_variant = self.db_client.create_product_variant(
                created_product.id,
                ProductVariantTableBase.model_validate(
                    variant.model_dump(exclude_none=True)
                ),
            )
            variant.id = created_variant.id
            for config_attribute in variant.config_attributes:
                self.db_client.create_config_attribute(
                    created_variant.id,
                    ConfigAttributeTable.model_validate(config_attribute.model_dump()),
                )
        self.db_client.commit_changes()
        return product
