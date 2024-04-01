import os

from sqlalchemy import create_engine
from sqlmodel import select
from sqlmodel import Session

from src.models.product import Product2VariantsTable
from src.models.product import ProductTableBase
from src.models.product import ProductVariantTableBase

DATABASE_URL = os.getenv("DATABASE_URL")


class PostgresClient:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.session = Session(self.engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.engine.dispose()

    def create_product(self, product: ProductTableBase):
        try:
            self.session.add(product)
            self.session.commit()
        except Exception as ex:
            print(ex)
        return product

    def get_all_products(self) -> list[ProductTableBase]:
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
