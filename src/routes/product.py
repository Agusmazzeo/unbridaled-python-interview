from fastapi import Depends
from fastapi.routing import APIRouter

from src.clients.postgres_client import PostgresClient
from src.models.product import Product
from src.models.product import ProductTableBase

router = APIRouter()


@router.get("/all", response_model=list[Product])
def get_all_products(db_client: PostgresClient = Depends()):
    return db_client.get_all_products()


@router.post("/create", response_model=Product)
def create_product(new_product: Product, db_client: PostgresClient = Depends()):
    product_data = ProductTableBase.model_validate(new_product)
    return db_client.create_product(product_data)
