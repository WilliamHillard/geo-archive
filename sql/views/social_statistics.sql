-- View, some social statistics for every country over time

create view social_statistics as
with all_country_years as (
	select iso3, year from asylum_seekers
	union
	select iso3, year from intentional_homicides
	union
	select iso3, year from internet_users
	union
	select iso3, year from life_expectancy
	union
	select iso3, year from literacy_rate
	union
	select iso3, year from university_enrollment
)
select
	c.iso3 as "ISO3",
	c.country_name as "Country",
	c.region as "Region",
	c.income_level as "Income level",
	acy.year as "Year",
	a.asylum_seekers as "Asylum seekers",
	hom.intentional_homicides as "Intentional homicides",
	int.internet_users as "Internet users",
	life.life_expectancy as "Life expectancy",
	lit.literacy_rate as "Literacy rate",
	uni.university_enrollment as "University enrollment"
from countries c
join all_country_years acy
	on acy.iso3 = c.iso3
left join asylum_seekers a
	on acy.iso3 = a.iso3
	and acy.year = a.year
left join intentional_homicides hom
	on acy.iso3 = hom.iso3
	and acy.year = hom.year
left join internet_users int
	on acy.iso3 = int.iso3
	and acy.year = int.year
left join life_expectancy life
	on acy.iso3 = life.iso3
	and acy.year = life.year
left join literacy_rate lit
	on acy.iso3 = lit.iso3
	and acy.year = lit.year
left join university_enrollment uni
	on acy.iso3 = uni.iso3
	and acy.year = uni.year