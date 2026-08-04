-- Top 10 lowest GDP per capita countries (2025)

select 
	c.country_name as "Country",
	g.gdp,
	p.population as "Population",
	round(g.gdp / p.population) as "gdp per capita"
from countries c
join gdp g
	on c.iso3 = g.iso3
join population p
	on c.iso3 = p.iso3
	and p.year = g.year
where g.year = 2025
order by "gdp per capita" asc
limit 10;