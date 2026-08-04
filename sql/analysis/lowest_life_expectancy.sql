-- Highest life expectancy per country (1970)

select 
	c.country_name as "Country",
	round(cast(l.life_expectancy as numeric), 2) as "Life expectancy"
from countries c
join life_expectancy l
	on c.iso3 = l.iso3 
where l.year = 1970
order by l.life_expectancy asc
limit 10;
