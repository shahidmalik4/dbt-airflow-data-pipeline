{{ config(materialized='table') }}

with orders as (
    select
        order_id,
        order_date,
        order_priority
    from {{ ref('stg_orders') }}
),

line_items as (
    select
        order_id,
        ship_date,
        commit_date
    from {{ ref('stg_lineitems') }}
)

select
    o.order_id,
    o.order_date,
    o.order_priority,
    min(li.ship_date - o.order_date) as delivery_days,
    case
        when min(li.ship_date) <= min(li.commit_date) then true
        else false
    end as on_time_delivery
from orders o
join line_items li on o.order_id = li.order_id
group by 1, 2, 3
