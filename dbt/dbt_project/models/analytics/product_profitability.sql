{{ config(materialized='table') }}

with parts as (
    select
        part_id,
        name
    from {{ ref('stg_part') }}
),

line_items as (
    select
        part_id,
        extended_price,
        quantity
    from {{ ref('stg_lineitems') }}
)

select
    p.part_id,
    p.name as product_name,
    sum(li.quantity) as total_quantity_sold,
    sum(li.extended_price) as gross_revenue,
    sum(li.extended_price) / nullif(sum(li.quantity), 0) as avg_unit_price
from parts p
join line_items li on p.part_id = li.part_id
group by 1, 2
