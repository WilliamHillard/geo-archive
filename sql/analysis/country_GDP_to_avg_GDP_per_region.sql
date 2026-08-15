-- Country's GDP compared to the average GDP of its region

select
	c.country_name as "Country",
	c.region as "Region",
	round(g.gdp::numeric, 0) as "GDP",
	round(avg(g.gdp) over(partition by c.region)::numeric, 0) as "Regional avg GDP",
	round(g.gdp / round(avg(g.gdp) over(partition by c.region)::numeric, 0) * 100, 2) as "Country GDP compared to region avg GDP (%)"
from countries c
join gdp g
	on c.iso3 = g.iso3
where year = 2020
order by c.region, g.gdp desc;