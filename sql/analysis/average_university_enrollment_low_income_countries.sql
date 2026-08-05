-- Average university enrollment of all low income countries every year

select u.year as "Year",
	avg(u.university_enrollment) as "University enrollment rate"
from countries c
join university_enrollment u
	on c.iso3 = u.iso3
where c.income_level = 'Low income'
group by u.year
order by year asc;