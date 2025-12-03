-- Top products by revenue and quantity sold.

select
    p.part_id,
    p.name as part_name,
    sum(l.extended_price * (1 - l.discount)) as revenue,
    sum(l.quantity) as quantity_sold,
    row_number() over (order by sum(l.extended_price * (1 - l.discount)) desc) as rank_by_revenue
from {{ ref('stg_lineitems') }} l
left join {{ ref('stg_part') }} p on l.part_id = p.part_id
group by 1,2
order by revenue desc
