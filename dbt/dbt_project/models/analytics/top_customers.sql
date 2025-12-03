-- Customers ranked by lifetime revenue and orders count

select
    c.customer_id,
    c.name as customer_name,
    count(distinct o.order_id) as orders_count,
    sum(o.total_price) as lifetime_revenue,
    row_number() over (order by sum(o.total_price) desc) as customer_rank
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c on o.customer_id = c.customer_id
group by 1,2
order by lifetime_revenue desc
