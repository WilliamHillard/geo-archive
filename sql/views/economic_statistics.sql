-- View, some economic statistics for every country over time

create view economic_statistics as
with all_country_years as (
	select iso3, year from gdp
	union
	select iso3, year from inflation
	union
	select iso3, year from unemployment
)
select 
	c.iso3 as "ISO3",
	c.country_name as "Country",
	c.region as "Region",
	acy.year as "Year",
	g.gdp as "GDP",
	i.inflation as "Inflation",
	u.unemployment as "Unemployment"
from countries c
join all_country_years acy
	on c.iso3 = acy.iso3
left join gdp g
	on acy.iso3 = g.iso3
	and acy.year = g.year
left join inflation i
	on acy.iso3 = i.iso3
	and acy.year = i.year
left join unemployment u
	on acy.iso3 = u.iso3
	and acy.year = u.year