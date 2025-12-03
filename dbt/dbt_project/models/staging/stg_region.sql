
with region as (
    select * from {{ source('raw', 'region') }}
)

select
    r_regionkey as region_id,
    r_name as name,
    r_comment as comment
from region
