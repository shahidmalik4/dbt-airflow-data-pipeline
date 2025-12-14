from fastapi import APIRouter, Query, Response
from typing import List
from pydantic import conint
import logging

from ..utils.db import run_query
from ..schemas.analytics import (
    AvgOrderValue,
    CustomerLTV,
    OrdersOverTime,
    RevenueByRegion,
    TopCustomers,
    TopProducts,
    ProductProfitability,
    SupplierPerformance,
    RegionalSalesPerformance,
    OrderFulfillmentEfficiency,
    CustomerCohortRetention,
    DailySales
)

router = APIRouter(prefix="/v1/analytics", tags=["Analytics"])
logger = logging.getLogger("analytics-api")


@router.get("/avg_order_value", response_model=List[AvgOrderValue])
async def get_avg_order_value(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT month, avg_order_value, revenue, orders_count
        FROM analytics.avg_order_value
        ORDER BY month DESC
        LIMIT :limit
    """
    logger.info(f"GET /avg_order_value limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/customer_ltv", response_model=List[CustomerLTV])
async def get_customer_ltv(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT customer_id, cohort_month, lifetime_revenue
        FROM analytics.customer_ltv
        ORDER BY lifetime_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /customer_ltv limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/orders_over_time", response_model=List[OrdersOverTime])
async def get_orders_over_time(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT order_date, month, orders_count, revenue
        FROM analytics.orders_over_time
        ORDER BY month DESC
        LIMIT :limit
    """
    logger.info(f"GET /orders_over_time limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/revenue_by_region", response_model=List[RevenueByRegion])
async def get_revenue_by_region(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT month, region_name, nation_name, orders_count, revenue
        FROM analytics.revenue_by_region
        ORDER BY revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /revenue_by_region limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/top_customers", response_model=List[TopCustomers])
async def get_top_customers(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT customer_id, customer_name, orders_count, lifetime_revenue, customer_rank
        FROM analytics.top_customers
        ORDER BY lifetime_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /top_customers limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/top_products", response_model=List[TopProducts])
async def get_top_products(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT part_id, part_name, revenue, quantity_sold, rank_by_revenue
        FROM analytics.top_products
        ORDER BY revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /top_products limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/product_profitability", response_model=List[ProductProfitability])
async def get_product_profitability(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT part_id, product_name, gross_revenue, total_quantity_sold
        FROM analytics.product_profitability
        ORDER BY gross_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /product_profitability limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/supplier_performance", response_model=List[SupplierPerformance])
async def get_supplier_performance(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT supplier_id, supplier_name, total_orders, total_revenue, late_delivery_rate
        FROM analytics.supplier_performance_metrics
        ORDER BY total_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /supplier_performance limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/regional_sales_performance", response_model=List[RegionalSalesPerformance])
async def get_regional_sales_performance(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT region_name, nation_name, total_orders, total_revenue
        FROM analytics.regional_sales_performance
        ORDER BY total_revenue DESC
        LIMIT :limit
    """
    logger.info(f"GET /regional_sales_performance limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/order_fulfillment_efficiency", response_model=List[OrderFulfillmentEfficiency])
async def get_order_fulfillment_efficiency(limit: conint(gt=0, le=100) = Query(50)):
    sql = """
        SELECT order_id, order_date, delivery_days, on_time_delivery
        FROM analytics.order_fulfillment_efficiency
        ORDER BY order_date DESC
        LIMIT :limit
    """
    logger.info(f"GET /order_fulfillment_efficiency limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)


@router.get("/customer_cohort_retention", response_model=List[CustomerCohortRetention])
async def get_customer_cohort_retention():
    sql = """
        SELECT cohort_month, months_since_first_order, active_customers
        FROM analytics.customer_cohort_retention
        ORDER BY cohort_month, months_since_first_order
    """
    logger.info("GET /customer_cohort_retention")
    results = await run_query(sql)
    return results or Response(status_code=204)


@router.get("/daily_sales", response_model=List[DailySales])
async def get_daily_sales(
    limit: conint(gt=0, le=365) = Query(90)
):
    sql = """
        SELECT sales_date, total_orders, total_revenue, avg_line_revenue
        FROM analytics.daily_sales
        ORDER BY sales_date DESC
        LIMIT :limit
    """
    logger.info(f"GET /daily_sales limit={limit}")
    results = await run_query(sql, {"limit": limit})
    return results or Response(status_code=204)