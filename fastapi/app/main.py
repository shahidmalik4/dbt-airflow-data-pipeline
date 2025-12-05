from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
import os

from .routers.dims_router import router as dims_router
from .routers.facts_router import router as facts_router
from .routers.kpis_router import router as kpis_router
from .routers.dbt_metadata import router as dbt_router

from .utils.logging import logger
from .utils.db import database

app = FastAPI(
    title="Analytics Data API",
    description="API exposing dimensional, fact, and KPI models from transformed schema",
    version="1.0.0",
    openapi_tags=[
        {"name": "Dimensions", "description": "Dimensional models endpoints"},
        {"name": "Facts", "description": "Fact models endpoints"},
        {"name": "Analytics", "description": "Analytics Metrics Endpoints"},
        {"name": "DBT", "description": "Endpoints for DBT metadata like status and execution time"},
    ],
    docs_url="/docs",
    redoc_url="/redoc"
)

router = APIRouter()

# Register routers
app.include_router(dims_router)
app.include_router(facts_router)
app.include_router(kpis_router)
app.include_router(dbt_router)

@router.get("/dbt/debug")
async def debug_dbt_path():
    return {
        "DBT_TARGET_PATH": str(DBT_TARGET_PATH),
        "run_results_exists": (DBT_TARGET_PATH / "run_results.json").exists(),
        "manifest_exists": (DBT_TARGET_PATH / "manifest.json").exists()
    }


@app.on_event("startup")
async def on_startup():
    logger.info("Connecting to database...")
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Disconnecting from database...")
    await database.disconnect()
