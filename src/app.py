import datetime

from fastapi import FastAPI

from src import __version__
from src.routes.probes import router as probes_router
from src.routes.product import router as product_router


app = FastAPI(
    title="Unbridaled API",
    description="Unbridaled Test API",
    version=__version__,
    **{"APP_VERSION": __version__, "STARTUP_DATETIME": datetime.datetime.now(datetime.UTC)},  # type: ignore
)

app.include_router(
    probes_router,
    prefix="/api/v1",
)

app.include_router(product_router, prefix="/api/v1/products")
