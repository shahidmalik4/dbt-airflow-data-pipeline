from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import date, datetime
from decimal import Decimal

# -------------------
# Marts / Dim Tables
# -------------------
class DimCustomer(BaseModel):
    customer_id: int
    name: str
    address: Optional[str] = None
    nation_id: Optional[int] = None
    nation: Optional[str] = None
    region: Optional[str] = None
    phone: Optional[str] = None
    account_balance: Optional[Decimal] = None
    market_segment: Optional[str] = None

class DimPart(BaseModel):
    part_id: int
    name: str
    manufacturer: Optional[str] = None
    brand: Optional[str] = None
    type: Optional[str] = None
    size: Optional[Union[str, int]] = None
    container: Optional[str] = None
    retail_price: Optional[Decimal] = None

class DimPartsupp(BaseModel):
    part_id: int
    supplier_id: int
    available_qty: Optional[int] = None
    supply_cost: Optional[Decimal] = None


class DimSupplier(BaseModel):
    supplier_id: int
    name: str
    address: Optional[str] = None
    nation_id: Optional[int] = None
    nation: Optional[str] = None
    region: Optional[str] = None
    phone: Optional[str] = None
    account_balance: Optional[Decimal] = None

# -------------------
# Marts / Fact Tables
# -------------------
class FactOrders(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    total_price: Optional[Decimal] = None
    total_items: Optional[int] = None
    total_amount_after_discount: Optional[Decimal] = None
    total_tax: Optional[Decimal] = None

class FactLineItem(BaseModel):
    order_id: int
    line_number: int
    part_id: int
    supplier_id: int
    quantity: int
    extended_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    line_status: Optional[str] = None
    price_after_discount: Optional[Decimal] = None

# -------------------
# Analytics / Aggregated Views
# -------------------
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

# -------------------
# DBT Metadata Models
# -------------------
class DBTModelStatus(BaseModel):
    unique_id: str
    status: str
    execution_time: float

class DBTMetadata(BaseModel):
    last_run: str
    models_status: List[DBTModelStatus]
    manifest_summary: dict
    freshness: dict