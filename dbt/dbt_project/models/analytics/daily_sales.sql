{{ config(materialized='table') }}

with orders as (
    select
        order_id,
        order_date
    from {{ ref('stg_orders') }}
),

line_items as (
    select
        order_id,
        extended_price
    from {{ ref('stg_lineitems') }}
)

select
    o.order_date as sales_date,
    count(distinct o.order_id) as total_orders,
    sum(li.extended_price) as total_revenue,
    avg(li.extended_price) as avg_line_revenue
from orders o
join line_items li
    on o.order_id = li.order_id
group by 1
