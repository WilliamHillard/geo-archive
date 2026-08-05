-- Number of conutries per region

select c.region as "Region",
	count(c.region) as "Number of countries per region"
from countries c
group by c.region
order by "Number of countries per region" desc;