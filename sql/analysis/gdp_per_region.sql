-- The total GDP of each region (2020)

select c.region as "Region",
	sum(round(g.gdp / 1000000000)) as "Total GDP of region (billions of dollars)"
from countries c
join gdp g
	on c.iso3 = g.iso3
where g.year = 2020
group by c.region
order by "Total GDP of region (billions of dollars)" desc;