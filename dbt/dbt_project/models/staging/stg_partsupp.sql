
with partsupp as (
    select * from {{ source('raw', 'partsupp') }}
)

select
    ps_partkey      as part_id,
    ps_suppkey      as supplier_id,
    ps_availqty     as available_qty,
    ps_supplycost   as supply_cost,
    ps_comment      as comment
from partsupp
