-- Top 10 largest countries by surface area (2023)

select 
	c.country_name, 
	s.surface_area
from countries c
join surface_area s
	on c.iso3 = s.iso3
where s.year = 2023
order by s.surface_area desc
limit 10;