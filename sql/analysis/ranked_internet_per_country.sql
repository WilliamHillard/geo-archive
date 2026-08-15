-- The highest internet usage between year 2000-2020 for every country

with ranked_internet as (
	select
		c.country_name as country,
		i.year as year,
		i.internet_users as internet_users,
		rank() over(partition by i.iso3 order by i.internet_users desc) as rank
	from countries c
	join internet_users i
		on c.iso3 = i.iso3
	where i.year between 2000 and 2020)
select
	country as "Country",
	year as "Year",
	round(internet_users::numeric, 2) as "Internet users (%)"
from ranked_internet
	where rank = 1
order by internet_users desc