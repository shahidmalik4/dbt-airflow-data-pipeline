
with customers as(
	select * from {{ source('raw', 'customer')}}
)

select
    c_custkey     as customer_id,
    c_name        as name,
    c_address     as address,
    c_nationkey   as nation_id,
    c_phone       as phone,
    c_acctbal     as account_balance,
    c_mktsegment  as market_segment
from customers