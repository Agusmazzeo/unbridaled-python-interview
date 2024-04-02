from fastapi.routing import APIRouter

from src.models.schemas import AliveResponse

router = APIRouter()


@router.get("/alive", response_model=AliveResponse, status_code=200)
def alive():
    return {"alive": True}
