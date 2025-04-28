from fastapi import APIRouter, Security

from app.infra.api.auth import get_api_key
from app.api.v1.endpoints import health
from app.api.v1.endpoints import intervals

routers = APIRouter()

routers.include_router(
    health.router,
    tags=["health", "healthcheck"],
    prefix="/healthcheck"
)

routers.include_router(
    intervals.router,
    tags=["intervals",  "max", "min"],
    prefix="/intervals",
    dependencies=[Security(get_api_key)]
)
