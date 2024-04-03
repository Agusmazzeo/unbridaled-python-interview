import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.models.schemas import ProductCreateSchema


@pytest.fixture
def product_to_create() -> ProductCreateSchema:
    with open("tests/test_files/complete_product.json") as f:
        return ProductCreateSchema.model_validate_json(f.read())


class TestProductRoutes:

    client = TestClient(app)
    routes_prefix = "api/v1/products"

    @pytest.mark.integration
    @pytest.mark.usefixtures("postgres_test_db")
    def test_get_all_products(self):
        response = self.client.get(f"{self.routes_prefix}/all")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.integration
    @pytest.mark.usefixtures("postgres_test_db")
    def test_get_unexistent_product(self):
        response = self.client.get(f"{self.routes_prefix}/1000")
        assert response.status_code == 404

    @pytest.mark.integration
    @pytest.mark.usefixtures("postgres_test_db")
    def test_create_and_get_product(self, product_to_create: ProductCreateSchema):
        response = self.client.post(
            f"{self.routes_prefix}/create",
            json=product_to_create.model_dump(exclude_none=True),
        )
        assert response.status_code == 201
        response_json = response.json()
        assert response_json["id"] is not None
        product_id = response_json["id"]
        assert response_json["name"] == "Standard-hilt lightsaber"
        assert response_json["uom"] == "pcs"
        assert len(response_json["variants"]) == 1

        response = self.client.get(f"{self.routes_prefix}/{product_id}")
        assert response.status_code == 200
