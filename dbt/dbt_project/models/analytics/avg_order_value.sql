-- Average order value (AOV) by month

with ord as (
    select
        order_id,
        order_date::date as order_date,
        total_price
    from {{ ref('stg_orders') }}
)

select
    date_trunc('month', order_date)::date as month,
    avg(total_price) as avg_order_value,
    sum(total_price) as revenue,
    count(*) as orders_count
from ord
group by 1
order by 1
