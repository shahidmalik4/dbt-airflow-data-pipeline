{{ config(materialized='table') }}

with suppliers as (
    select
        supplier_id,
        name
    from {{ ref('stg_supplier') }}
),

line_items as (
    select
        supplier_id,
        order_id,
        ship_date,
        commit_date,
        extended_price
    from {{ ref('stg_lineitems') }}
)

select
    s.supplier_id,
    s.name as supplier_name,
    count(distinct li.order_id) as total_orders,
    sum(li.extended_price) as total_revenue,
    avg(ship_date - commit_date) as avg_delivery_days,
    sum(
        case when ship_date > commit_date then 1 else 0 end
    )::float / count(*) as late_delivery_rate
from suppliers s
join line_items li on s.supplier_id = li.supplier_id
group by 1, 2
