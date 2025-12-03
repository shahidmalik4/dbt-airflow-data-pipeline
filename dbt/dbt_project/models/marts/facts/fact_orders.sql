select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_price,
    count(l.line_number) as total_items,
    sum(l.extended_price * (1 - l.discount)) as total_amount_after_discount,
    sum(l.tax) as total_tax
from {{ ref('stg_orders') }} o
join {{ ref('stg_lineitems') }} l
    on o.order_id = l.order_id
group by o.order_id, o.customer_id, o.order_date, o.total_price
