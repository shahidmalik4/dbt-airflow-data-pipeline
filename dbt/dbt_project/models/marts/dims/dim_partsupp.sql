select
    ps.part_id,
    ps.supplier_id,
    ps.available_qty,
    ps.supply_cost
from {{ ref('stg_partsupp') }} ps