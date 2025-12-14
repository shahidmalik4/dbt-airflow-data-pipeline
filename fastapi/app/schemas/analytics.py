from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


class AvgOrderValue(BaseModel):
    month: Optional[date] = None
    avg_order_value: Optional[Decimal] = None
    revenue: Optional[Decimal] = None
    orders_count: Optional[int] = None

class CustomerLTV(BaseModel):
    customer_id: int
    cohort_month: Optional[date] = None
    lifetime_revenue: Optional[Decimal] = None

class OrdersOverTime(BaseModel):
    order_date: Optional[date] = None
    month: Optional[str] = None
    orders_count: Optional[int] = None
    revenue: Optional[Decimal] = None

class RevenueByRegion(BaseModel):
    month: Optional[date] = None
    region_name: str
    nation_name: Optional[str] = None
    orders_count: Optional[int] = None
    revenue: Optional[Decimal] = None

class TopCustomers(BaseModel):
    customer_id: int
    customer_name: str
    orders_count: Optional[int] = None
    lifetime_revenue: Optional[Decimal] = None
    customer_rank: Optional[int] = None

class TopProducts(BaseModel):
    part_id: int
    part_name: str
    revenue: Optional[Decimal] = None
    quantity_sold: Optional[int] = None
    rank_by_revenue: Optional[int] = None

class ProductProfitability(BaseModel):
    part_id: int
    product_name: str
    gross_revenue: Optional[Decimal] = None
    total_quantity_sold: Optional[int] = None

class SupplierPerformance(BaseModel):
    supplier_id: int
    supplier_name: str
    total_orders: Optional[int] = None
    total_revenue: Optional[Decimal] = None
    late_delivery_rate: Optional[Decimal] = None

class RegionalSalesPerformance(BaseModel):
    region_name: str
    nation_name: Optional[str] = None
    total_orders: Optional[int] = None
    total_revenue: Optional[Decimal] = None

class OrderFulfillmentEfficiency(BaseModel):
    order_id: int
    order_date: Optional[date] = None
    delivery_days: Optional[int] = None
    on_time_delivery: Optional[bool] = None

class CustomerCohortRetention(BaseModel):
    cohort_month: date
    months_since_first_order: int
    active_customers: int

class DailySales(BaseModel):
    sales_date: date
    total_orders: Optional[int] = None
    total_revenue: Optional[Decimal] = None
    avg_line_revenue: Optional[Decimal] = None
