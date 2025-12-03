-- Top products by revenue and quantity sold.

select
    dp.part_key,
    dp.part_name,
    sum(fl.net_price) as revenue,
    sum(fl.quantity) as quantity_sold,
    row_number() over (order by sum(fl.net_price) desc) as rank_by_revenue
from {{ ref('fact_lineitem') }} fl
left join {{ ref('dim_part') }} dp on fl.part_key = dp.part_key
group by 1, 2
order by revenue desc