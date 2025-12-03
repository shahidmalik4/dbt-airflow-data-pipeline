-- Time series of orders (daily + monthly) for trend charts.

with orders as(
	select
		order_id,
		order_date::date as order_date,
		total_price
	from {{ ref('stg_orders')}}
)

select
	order_date,
	date_trunc('month', order_date)::date as month,
	count(distinct order_id) as orders_count,
	sum(total_price) as revenue
from orders
group by 1, 2
order by 1