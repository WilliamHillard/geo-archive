-- Population growth (1970-2025) among countries with over 50 milion people

select c.country_name as "Country",
	p1970.population as "1970",
	p2025.population as "2025",
	p2025.population - p1970.population as "Population growth"
from countries c
join population p1970
	on c.iso3 = p1970.iso3
	and p1970.year = 1970
join population p2025
	on c.iso3 = p2025.iso3
	and p2025.year = 2025
where p2025.population > 50000000
order by "Population growth" desc;