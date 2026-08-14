-- Rank countries by population within each region in 2025

select c.country_name as "Country",
	c.region as "Region",
	p.population as "Population",
	rank() over(partition by c.region order by p.population desc) as "Population rank"
from countries c
join population p
	on c.iso3 = p.iso3
where p.year = 2025
order by c.region, "Population rank";