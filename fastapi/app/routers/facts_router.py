from fastapi import APIRouter, HTTPException, Query, Response
from typing import List
from pydantic import conint
import logging

from ..utils.db import run_query
from ..schemas.facts import FactOrders, FactLineItem

router = APIRouter(prefix="/v1/facts", tags=["Facts"])
logger = logging.getLogger("analytics-api")


@router.get("/orders", response_model=List[FactOrders])
async def get_fact_orders(
    limit: conint(gt=0, le=100) = Query(50),
    sort_by: str = Query("order_date"),
    sort_order: str = Query("desc")
):
    valid_sort_fields = {
        "order_id", "customer_id", "order_date",
        "total_price", "total_items", "total_amount_after_discount", "total_tax"
    }
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    sql = f"""
        SELECT order_id, customer_id, order_date, total_price, total_items,
               total_amount_after_discount, total_tax
        FROM marts.fact_orders
        ORDER BY {sort_by} {direction}
        LIMIT :limit
    """
    logger.info(f"GET /v1/facts/orders?limit={limit}&sort_by={sort_by}&sort_order={sort_order}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/lineitems", response_model=List[FactLineItem])
async def get_fact_lineitems(
    limit: conint(gt=0, le=100) = Query(50),
    sort_by: str = Query("order_id"),
    sort_order: str = Query("asc")
):
    valid_sort_fields = {
        "order_id", "line_number", "part_id", "supplier_id",
        "quantity", "extended_price", "discount", "tax",
        "line_status", "price_after_discount"
    }
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    sql = f"""
        SELECT order_id, line_number, part_id, supplier_id,
               quantity, extended_price, discount, tax,
               line_status, price_after_discount
        FROM marts.fact_lineitem
        ORDER BY {sort_by} {direction}
        LIMIT :limit
    """
    logger.info(f"GET /v1/facts/lineitems?limit={limit}&sort_by={sort_by}&sort_order={sort_order}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)
