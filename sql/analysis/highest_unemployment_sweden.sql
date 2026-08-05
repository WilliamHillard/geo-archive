-- Highest unemployment rate years in Sweden

select 
	c.country_name as "Country",
	u.unemployment as "Unemployment",
	u.year as "Year"
from countries c
join unemployment u
	on c.iso3 = u.iso3
where c.country_name = 'Sweden'
order by u.unemployment desc
limit 10;