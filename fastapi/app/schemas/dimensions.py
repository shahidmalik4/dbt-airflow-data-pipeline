from pydantic import BaseModel
from typing import Optional, Union
from decimal import Decimal


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