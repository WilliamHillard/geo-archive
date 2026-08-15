-- Every countries population and changes per year

with population_changes as (
	select 
		c.country_name as country,
	    p.year as year,
	    p.population as population,
	    lag(p.population) over (partition by p.iso3 order by p.year) as previous_population
	from countries c
	join population p
		on c.iso3 = p.iso3)
select
    country,
    year,
    population,
    previous_population,
    population - previous_population as "Population change",
    round(((population - previous_population) / previous_population::numeric) * 100, 2) as "Population growth (%)"
from population_changes
order by country, year;