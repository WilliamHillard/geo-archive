-- Top 10 countries by population year 2025

select c.country_name, p.population
from countries c
join population p
on c.iso3 = p.iso3
where p.year = 2025
order by p.population desc
limit 10;