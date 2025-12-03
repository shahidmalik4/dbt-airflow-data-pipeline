select
    l.order_id,
    l.line_number,
    l.part_id,
    l.supplier_id,
    l.quantity,
    l.extended_price,
    l.discount,
    l.tax,
    l.line_status,
    (l.extended_price * (1 - l.discount)) as price_after_discount
from {{ ref('stg_lineitems') }} l
