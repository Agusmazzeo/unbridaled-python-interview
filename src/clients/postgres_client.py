import os

from sqlalchemy import create_engine
from sqlmodel import select
from sqlmodel import Session

from src.exceptions import ConnectionFailure
from src.exceptions import QueryFailure
from src.models.product import ConfigAttributeTable
from src.models.product import Product2VariantsTable
from src.models.product import ProductTableBase
from src.models.product import ProductVariant2ConfigAttributeTable
from src.models.product import ProductVariantTableBase

DATABASE_URL = os.getenv("DATABASE_URL")


class PostgresClient:
    def __init__(self):
        try:
            self.engine = create_engine(DATABASE_URL)
            self.session = Session(self.engine)
        except:
            raise ConnectionFailure("Could not connect to the database")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.engine.dispose()

    def commit_changes(self):
        self.session.commit()

    def create_product(self, product: ProductTableBase) -> ProductTableBase:
        try:
            self.session.add(product)
            self.session.flush()
            return product
        except Exception as ex:
            self.session.rollback()
            raise QueryFailure(f"Failed to create product: {ex}")

    def create_product_variant(
        self, product_id: int, variant: ProductVariantTableBase
    ) -> ProductVariantTableBase:
        try:
            self.session.add(variant)
            self.session.flush()

            self.session.add(
                Product2VariantsTable(product_id=product_id, variant_id=variant.id)
            )
            self.session.flush()
            return variant
        except Exception as ex:
            self.session.rollback()
            raise QueryFailure(f"Failed to create product variant: {ex}")

    def create_config_attribute(
        self, variant_id: int, config_attribute: ConfigAttributeTable
    ) -> ConfigAttributeTable:
        try:
            existent_config = self.get_config_attribute(config_attribute)
            if existent_config is None:
                self.session.add(config_attribute)
                self.session.flush()
            else:
                config_attribute = existent_config

            self.session.add(
                ProductVariant2ConfigAttributeTable(
                    product_variant_id=variant_id,
                    config_attribute_id=config_attribute.id,
                )
            )
            self.session.flush()
            return config_attribute
        except Exception as ex:
            self.session.rollback()
            raise QueryFailure(f"Failed to create config attribute: {ex}")

    def get_config_attribute(
        self, config_attribute: ConfigAttributeTable
    ) -> ConfigAttributeTable | None:
        try:
            statement = select(ConfigAttributeTable).where(
                ConfigAttributeTable.config_name == config_attribute.config_name,
                ConfigAttributeTable.config_value == config_attribute.config_value,
            )
            result = [a for a in self.session.exec(statement)]
            return result[0] if len(result) > 0 else None
        except Exception as ex:
            raise QueryFailure(f"Failed to execute query: {ex}")

    def get_product_by_id(
        self, product_id: int
    ) -> list[tuple[ProductTableBase, ProductVariantTableBase]]:
        try:
            statement = (
                select(ProductTableBase, ProductVariantTableBase)
                .join_from(
                    ProductTableBase,
                    Product2VariantsTable,
                    ProductTableBase.id == Product2VariantsTable.product_id,
                    isouter=True,
                )
                .join_from(
                    Product2VariantsTable,
                    ProductVariantTableBase,
                    ProductVariantTableBase.id == Product2VariantsTable.variant_id,
                    isouter=True,
                )
                .where(ProductTableBase.id == product_id)
            )
            return self.session.exec(statement)
        except Exception as ex:
            raise QueryFailure(f"Failed to execute query: {ex}")

    def get_all_products_with_variations(
        self,
    ) -> list[tuple[ProductTableBase, ProductVariantTableBase]]:
        try:
            statement = (
                select(ProductTableBase, ProductVariantTableBase)
                .join_from(
                    ProductTableBase,
                    Product2VariantsTable,
                    ProductTableBase.id == Product2VariantsTable.product_id,
                    isouter=True,
                )
                .join_from(
                    Product2VariantsTable,
                    ProductVariantTableBase,
                    ProductVariantTableBase.id == Product2VariantsTable.variant_id,
                    isouter=True,
                )
            )
            return self.session.exec(statement)
        except Exception as ex:
            raise QueryFailure(f"Failed to execute query: {ex}")
