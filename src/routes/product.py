from fastapi import Depends
from fastapi import HTTPException
from fastapi.routing import APIRouter

from src.clients.postgres_client import PostgresClient
from src.handlers.product import ProductHandler
from src.models.product import Product
from src.models.schemas import ProductCreateSchema
from src.models.schemas import ProductResponseSchema

router = APIRouter()


@router.get("/all", response_model=list[ProductResponseSchema])
def get_all_products(db_client: PostgresClient = Depends()):
    return ProductHandler(db_client).get_all_products_with_variatiants()


@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product_by_id(product_id: int, db_client: PostgresClient = Depends()):
    product = ProductHandler(db_client).get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/create", response_model=ProductCreateSchema, status_code=201)
def create_product(
    new_product: ProductCreateSchema, db_client: PostgresClient = Depends()
):
    return ProductHandler(db_client).create_product(
        Product.model_validate(new_product.model_dump())
    )
