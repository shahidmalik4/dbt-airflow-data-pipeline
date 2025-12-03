select
    p.part_id,
    p.name,
    p.manufacturer,
    p.brand,
    p.type,
    p.size,
    p.container,
    p.retail_price
from {{ ref('stg_part') }} p