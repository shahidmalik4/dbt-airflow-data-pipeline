-- Simplified customer lifetime value: total revenue per customer
-- Cohort is based on the customer's first order date.

with first_order as (
    select
        o.customer_id,
        min(o.order_date)::date as first_order_date
    from {{ ref('stg_orders') }} o
    group by o.customer_id
),

cust as (
    select
        c.customer_id,
        fo.first_order_date,
        date_trunc('month', fo.first_order_date)::date as cohort_month
    from {{ ref('stg_customers') }} c
    left join first_order fo
        on c.customer_id = fo.customer_id
),

cust_revenue as (
    select
        o.customer_id,
        sum(o.total_price) as revenue
    from {{ ref('stg_orders') }} o
    group by o.customer_id
)

select
    c.customer_id,
    c.cohort_month,
    coalesce(cr.revenue, 0) as lifetime_revenue
from cust c
left join cust_revenue cr
    on c.customer_id = cr.customer_id
order by lifetime_revenue desc
