-- View, latest population for every country

create view latest_population as
select 
	c.country_name as "Country",
	p.year as "Year",
	p.population as "Population"
from countries c
join population p
	on c.iso3 = p.iso3
where p.year = (
	select max(year)
	from population
);