-- Which countries improved the most in life expectancy from 2000-2020

select c.country_name as "Country",
	l2000.life_expectancy as "2000",
	l2020.life_expectancy as "2020",
	round((l2020.life_expectancy - l2000.life_expectancy)::numeric, 2) as "Improved life expectancy 2000 to 2020"
from countries c
join life_expectancy l2000
	on c.iso3 = l2000.iso3
join life_expectancy l2020
	on c.iso3 = l2020.iso3
where l2000.year = 2000
	and l2020.year = 2020
order by "Improved life expectancy 2000 to 2020" desc
limit 30;