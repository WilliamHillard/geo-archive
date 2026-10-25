-- View, some demographic statistics of every country over time

create view demographic_statistics as
with all_country_years as (
	select iso3, year from population
	union
	select iso3, year from net_migration
	union
	select iso3, year from urban_population
)
select
	c.iso3 as "ISO3",
	c.country_name as "Country",
	c.region as "Region",
	acy.year as "Year",
	p.population as "Population",
	m.net_migration as "Net migration",
	urb.urban_population as "Urban population"
from countries c
join all_country_years acy
	on acy.iso3 = c.iso3
left join population p
	on acy.iso3 = p.iso3
	and acy.year = p.year
left join net_migration m
	on acy.iso3 = m.iso3
	and acy.year = m.year
left join urban_population urb
	on acy.iso3 = urb.iso3
	and acy.year = urb.year