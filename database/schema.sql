create table countries (
iso3 char(3) primary key not null,
country_name text not null
);

create table population (
iso3 char(3) not null,
year int not null,
population bigint not null,
primary key (iso3, year),
foreign key (iso3)
references countries(iso3)
);