-- Asylum seekers and intentional homicides correlation in Germany

select c.country_name,
	a.asylum_seekers as "Asylum seekers",
	i.intentional_homicides as "Intentional homicides",
	a.year
from countries c
join asylum_seekers a
	on c.iso3 = a.iso3 
join intentional_homicides i
	on c.iso3 = i.iso3 
	and a.year = i.year
where c.country_name = 'Germany'
order by a.year asc;