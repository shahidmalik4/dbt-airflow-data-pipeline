select
    c.customer_id,
    c.name,
    c.address,
    c.nation_id,
    n.name as nation,
    r.name as region,
    c.phone,
    c.account_balance,
    c.market_segment
from {{ ref('stg_customers') }} c
left join {{ ref('stg_nation') }} n
    on c.nation_id = n.nation_id
left join {{ ref('stg_region') }} r
    on n.region_id = r.region_id