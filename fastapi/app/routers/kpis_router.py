from fastapi import APIRouter, HTTPException, Query, Response
from typing import List
from pydantic import conint
import logging

from ..utils.db import run_query
from ..schemas import (
    AvgOrderValue,
    CustomerLTV,
    OrdersOverTime,
    RevenueByRegion,
    TopCustomers,
    TopProducts
)

router = APIRouter(prefix="/v1/analytics", tags=["Analytics"])
logger = logging.getLogger("analytics-api")

# -------------------------
# Average Order Value
# -------------------------
@router.get("/avg_order_value", response_model=List[AvgOrderValue])
async def get_avg_order_value(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT month, avg_order_value, revenue, orders_count
        FROM analytics.avg_order_value
        ORDER BY month DESC
        LIMIT :limit
    """
    logger.info(f"GET /v1/analytics/avg_order_value?limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)

# -------------------------
# Customer LTV
# -------------------------
@router.get("/customer_ltv", response_model=List[CustomerLTV])
async def get_customer_ltv(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT customer_id, cohort_month, lifetime_revenue
        FROM analytics.customer_ltv
        ORDER BY lifetime_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /v1/analytics/customer_ltv?limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)

# -------------------------
# Orders Over Time
# -------------------------
@router.get("/orders_over_time", response_model=List[OrdersOverTime])
async def get_orders_over_time(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT order_date, month, orders_count, revenue
        FROM analytics.orders_over_time
        ORDER BY month DESC
        LIMIT :limit
    """
    logger.info(f"GET /v1/analytics/orders_over_time?limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)

# -------------------------
# Revenue By Region
# -------------------------
@router.get("/revenue_by_region", response_model=List[RevenueByRegion])
async def get_revenue_by_region(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT month, region_name, nation_name, orders_count, revenue
        FROM analytics.revenue_by_region
        ORDER BY revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /v1/analytics/revenue_by_region?limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)

# -------------------------
# Top Customers
# -------------------------
@router.get("/top_customers", response_model=List[TopCustomers])
async def get_top_customers(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT customer_id, customer_name, orders_count, lifetime_revenue, customer_rank
        FROM analytics.top_customers
        ORDER BY lifetime_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /v1/analytics/top_customers?limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)

# -------------------------
# Top Products
# -------------------------
@router.get("/top_products", response_model=List[TopProducts])
async def get_top_products(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT part_id, part_name, revenue, quantity_sold, rank_by_revenue
        FROM analytics.top_products
        ORDER BY revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /v1/analytics/top_products?limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)