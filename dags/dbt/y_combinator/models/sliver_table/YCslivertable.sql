with transformation as (
    select 
        "name" as company,
        COALESCE(NULLIF("Description", ''), 'Unspecified') as value_proposition,
        coalesce(nullif(split(coalesce("Location", 'Remote'), ',')[0]::string, ''), 'Remote') as city,
        coalesce(split("Location", ',')[1]::string, 'Remote') as state,
        coalesce(split("Location", ',')[2]::string, 'World') as country,
        coalesce(split("tags", ',')[0]::string, 'Unspecified') as batch,
        coalesce(split("tags", ',')[1]::string, 'Unspecified') as customer_type,
        coalesce(split("tags", ',')[2]::string, 'Unspecified') as industry,
        coalesce(split("tags", ',')[3]::string, 'Unspecified') as additional_info,
        "tags" as other_info
    from {{ source('Y_Combinator', 'COMPAINES') }}
),
updated_transformation as (
    select 
        company,
        value_proposition,
        city,
        state,
        country,
        batch,
        customer_type,
         case
            when industry = 'Travel' then industry || ' Leisure and Tourism'
            when industry = 'Engineering' then industry || 'Product and Design'
            else industry
        end as industry,
    from transformation
)
select company, value_proposition, city, state, country, batch, customer_type, industry
from updated_transformation