{{ config(materialized='table') }}

with orders as (
    select
        customer_id,
        order_date 
    from {{ ref('stg_orders') }}
),

first_order as (
    select
        customer_id,
        min(order_date) as first_order_date
    from orders
    group by 1
),

cohorts as (
    select
        o.customer_id,
        date_trunc('month', f.first_order_date) as cohort_month,
        date_trunc('month', o.order_date) as order_month,
        extract(month from age(o.order_date, f.first_order_date)) as months_since_first_order
    from orders o
    join first_order f on o.customer_id = f.customer_id
)

select
    cohort_month,
    months_since_first_order,
    count(distinct customer_id) as active_customers
from cohorts
group by 1, 2
order by 1, 2
