-- View, static statistics for every country

create view static_country_statistics as
with latest_surface_area as (
	select s.*,
		row_number() over (
			partition by s.iso3
			order by s.year desc)
			as rn
		from surface_area s)
select
	c.iso3 as "ISO3",
	c.country_name as "Country",
	c.capital_city as "Capital city",
	c.region as "Region",
	c.longitude as "Longitude",
	c.latitude as "Latitude",
	s.surface_area as "Surface area (km²)"
from countries c
left join latest_surface_area s
	on c.iso3 = s.iso3
	and s.rn = 1