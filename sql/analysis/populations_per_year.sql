-- Every countries population and changes per year

select c.country_name as "Country",
    p.year as "Year",
    p.population as "Population",
    lag(p.population) over (partition by p.iso3 order by p.year) as "Previous population",
    p.population - lag(p.population) over (partition by p.iso3 order by p.year) as "Population change",
    round(((p.population - lag(p.population) over (partition by p.iso3 order by p.year)) / 
    lag(p.population) over (partition by p.iso3 order by p.year)::numeric) * 100, 2) as "Population growth (%)"
from countries c
join population p
    on c.iso3 = p.iso3
order by c.country_name, p.year;