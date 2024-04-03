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
            if not product_dict.get(product.id):
                product_dict[product.id] = Product.model_validate(product.model_dump())
            if variant is not None:
                product_dict[product.id].variants.append(
                    ProductVariant.model_validate(variant.model_dump())
                )
        return product_dict.values()

    def create_product(self, product: Product) -> Product:
        created_product = self.db_client.create_product(
            product=ProductTableBase.model_validate(product.model_dump())
        )
        product.id = created_product.id

        for variant in product.variants:
            created_variant = self.db_client.create_product_variant(
                created_product.id,
                ProductVariantTableBase.model_validate(variant.model_dump()),
            )
            variant.id = created_variant.id
            for config_attribute in variant.config_attributes:
                self.db_client.create_config_attribute(
                    created_variant.id,
                    ConfigAttributeTable.model_validate(config_attribute.model_dump()),
                )
        self.db_client.commit_changes()
        return product
