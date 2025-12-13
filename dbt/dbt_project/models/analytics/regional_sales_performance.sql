{{ config(materialized='table') }}

with customers as (
    select
        customer_id,
        nation_id
    from {{ ref('stg_customers') }}
),

nations as (
    select
        nation_id,
        name as nation_name,
        region_id
    from {{ ref('stg_nation') }}
),

regions as (
    select
        region_id,
        name as region_name
    from {{ ref('stg_region') }}
),

orders as (
    select
        order_id,
        customer_id
    from {{ ref('stg_orders') }}
),

line_items as (
    select
        order_id,
        extended_price
    from {{ ref('stg_lineitems') }}
)

select
    r.region_name,
    n.nation_name,
    sum(li.extended_price) as total_revenue,
    count(distinct o.order_id) as total_orders
from orders o
join customers c on o.customer_id = c.customer_id
join nations n on c.nation_id = n.nation_id
join regions r on n.region_id = r.region_id
join line_items li on o.order_id = li.order_id
group by 1, 2
