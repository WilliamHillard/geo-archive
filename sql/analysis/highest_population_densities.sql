-- Top 10 highest population densities (2025)

select 
	c.country_name as "Country",
    p.population as "Population",
    s.surface_area as "Surface area (km²)",
    round(p.population / s.surface_area) as "Population density (people/km²)"
from countries c
join population p
	on c.iso3 = p.iso3
join surface_area s
	on c.iso3 = s.iso3
where p.year = 2025
	and s.year = 2023
order by "Population density (people/km²)" desc
limit 10;