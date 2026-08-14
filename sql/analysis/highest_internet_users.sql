-- Highest internet users in South Asia between 2000-2020

select
    c.country_name as "Country",
    i.year as "Year",
    i.internet_users as "Highest internet usage"
from countries c
join internet_users i
    on c.iso3 = i.iso3
where c.region = 'South Asia'
  and i.year between 2000 and 2020
  and i.internet_users = (
      select MAX(i2.internet_users)
      from internet_users i2
      where i2.iso3 = i.iso3
        and i2.year between 2000 and 2020
  )
order by i.internet_users desc;