-- Countries per income level

select c.income_level as "Income level",
	count(c.country_name) as "Countries per income level"
from countries c
group by c.income_level
order by "Income level" asc