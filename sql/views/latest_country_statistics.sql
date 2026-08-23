-- View, latest statistics for every country

create view latest_country_statistics as
with latest_population as (
	select p.*,
		row_number() over (
			partition by p.iso3
			order by p.year desc)
			as rn
		from population p),
latest_gdp as (
	select g.*,
		row_number() over (
			partition by g.iso3
			order by g.year desc)
			as rn
		from gdp g),
latest_internet_users as (
	select int.*,
		row_number() over (
			partition by int.iso3
			order by int.year desc)
			as rn
		from internet_users int),
latest_life_expectancy as (
	select l.*,
		row_number() over (
			partition by l.iso3
			order by l.year desc)
			as rn
		from life_expectancy l),
latest_inflation as (
	select inf.*,
		row_number() over (
			partition by inf.iso3
			order by inf.year desc)
			as rn
		from inflation inf),
latest_urban_population as (
	select ur.*,
		row_number() over (
			partition by ur.iso3
			order by ur.year desc)
			as rn
		from urban_population ur)
select 
	c.iso3 as "ISO3",
	c.country_name as "Country",
	c.income_level as "Income level",
	p.year as "Population year",
	p.population as "Population",
	g.year as "GDP year",
	g.gdp as "GDP",
	int.year as "Internet users year",
	int.internet_users as "Internet users (%)",
	l.year as "Life expectancy year",
	l.life_expectancy as "Life expectancy",
	inf.year as "Inflation year",
	inf.inflation as "Inflation",
	ur.year as "Urban population year",
	ur.urban_population as "Urban population"
from countries c
left join latest_population p
	on c.iso3 = p.iso3
	and p.rn = 1
left join latest_gdp g
	on c.iso3 = g.iso3
	and g.rn = 1
left join latest_internet_users int
	on c.iso3 = int.iso3
	and int.rn = 1
left join latest_life_expectancy l
	on c.iso3 = l.iso3
	and l.rn = 1
left join latest_inflation inf
	on c.iso3 = inf.iso3
	and inf.rn = 1
left join latest_urban_population ur
	on c.iso3 = ur.iso3
	and ur.rn= 1