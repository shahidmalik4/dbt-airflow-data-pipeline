select
    s.supplier_id,
    s.name,
    s.address,
    s.nation_id,
    n.name as nation,
    r.name as region,
    s.phone,
    s.account_balance
from {{ ref('stg_supplier') }} s
left join {{ ref('stg_nation') }} n
    on s.nation_id = n.nation_id
left join {{ ref('stg_region') }} r
    on n.region_id = r.region_id