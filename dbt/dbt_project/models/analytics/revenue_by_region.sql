-- Revenue aggregated by region and month (joins dim_customer -> region)

with orders as (
    select
        o.order_id,
        o.customer_id,
        o.order_date::date as order_date,
        o.total_price
    from {{ ref('stg_orders') }} o
),

customers as (
    select
        c.customer_id,
        n.region_id,
        n.name as nation_name,
        r.name as region_name
    from {{ ref('stg_customers') }} c
    left join {{ ref('stg_nation') }} n on c.nation_id = n.nation_id
    left join {{ ref('stg_region') }} r on n.region_id = r.region_id
)

select
    date_trunc('month', o.order_date)::date as month,
    customers.region_name,
    customers.nation_name,
    count(distinct o.order_id) as orders_count,
    sum(o.total_price) as revenue
from orders o
join customers on customers.customer_id = o.customer_id
group by 1,2,3
order by 1 desc, 4 desc
