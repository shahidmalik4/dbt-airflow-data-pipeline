from fastapi import APIRouter, HTTPException, Query, Response
from typing import List
from pydantic import conint
import logging

from ..utils.db import run_query
from ..schemas.dimensions import DimCustomer, DimPart, DimPartsupp, DimSupplier

router = APIRouter(prefix="/v1/dimensions", tags=["Dimensions"])
logger = logging.getLogger("analytics-api")


@router.get("/customers", response_model=List[DimCustomer])
async def get_dim_customers(
    limit: conint(gt=0, le=100) = Query(50),
    sort_by: str = Query("customer_id"),
    sort_order: str = Query("desc")
):
    valid_sort_fields = {
        "customer_id", "name", "address", "nation_id", "nation", "region",
        "phone", "account_balance", "market_segment"
    }
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    sql = f"""
        SELECT customer_id, name, address, nation_id, nation, region, phone, account_balance, market_segment
        FROM marts.dim_customer
        ORDER BY {sort_by} {direction}
        LIMIT :limit
    """
    logger.info(f"GET /v1/dimensions/customers?limit={limit}&sort_by={sort_by}&sort_order={sort_order}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/parts", response_model=List[DimPart])
async def get_dim_parts(
    limit: conint(gt=0, le=100) = Query(50),
    sort_by: str = Query("name"),
    sort_order: str = Query("asc")
):
    valid_sort_fields = {"part_id", "name", "manufacturer", "brand", "type", "size", "container", "retail_price"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    sql = f"""
        SELECT part_id, name, manufacturer, brand, type, size, container, retail_price
        FROM marts.dim_part
        ORDER BY {sort_by} {direction}
        LIMIT :limit
    """
    logger.info(f"GET /v1/dimensions/parts?limit={limit}&sort_by={sort_by}&sort_order={sort_order}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/partsupp", response_model=List[DimPartsupp])
async def get_dim_partsupp(
    limit: conint(gt=0, le=100) = Query(50),
    sort_by: str = Query("part_id"),
    sort_order: str = Query("asc")
):
    valid_sort_fields = {"part_id", "supplier_id", "available_qty", "supply_cost"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    sql = f"""
        SELECT part_id, supplier_id, available_qty, supply_cost
        FROM marts.dim_partsupp
        ORDER BY {sort_by} {direction}
        LIMIT :limit
    """
    logger.info(f"GET /v1/dimensions/partsupp?limit={limit}&sort_by={sort_by}&sort_order={sort_order}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/suppliers", response_model=List[DimSupplier])
async def get_dim_suppliers(
    limit: conint(gt=0, le=100) = Query(50),
    sort_by: str = Query("supplier_id"),
    sort_order: str = Query("asc")
):
    valid_sort_fields = {"supplier_id", "name", "address", "nation_id", "nation", "region", "phone", "account_balance"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    sql = f"""
        SELECT supplier_id, name, address, nation_id, nation, region, phone, account_balance
        FROM marts.dim_supplier
        ORDER BY {sort_by} {direction}
        LIMIT :limit
    """
    logger.info(f"GET /v1/dimensions/suppliers?limit={limit}&sort_by={sort_by}&sort_order={sort_order}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)