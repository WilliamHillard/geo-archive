create table countries (
iso3 char(3) primary key not null,
iso2 char(2),
country_name text not null,
capital_city text,
region text,
income_level text,
longitude double precision,
latitude double precision,
lending_type text
);

create table population (
iso3 char(3) not null,
year int not null,
population bigint not null,
primary key (iso3, year),
foreign key (iso3) references countries(iso3)
);

create table gdp (
iso3 char(3) not null,
year int not null,
gdp numeric not null,
primary key (iso3, year),
foreign key (iso3) references countries(iso3)
);

create table life_expectancy (
iso3 char(3) not null,
year int not null,
life_expectancy float not null,
primary key (iso3, year),
foreign key (iso3) references countries(iso3)
);

create table surface_area (
iso3 char(3) not null,
year int not null,
surface_area float not null,
primary key (iso3, year),
foreign key (iso3) references countries(iso3)
);

create table urban_population (
iso3 char(3) not null,
year int not null,
urban_population float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table inflation (
iso3 char(3) not null,
year int not null,
inflation float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table intentional_homicides (
iso3 char(3) not null,
year int not null,
intentional_homicides float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table unemployment (
iso3 char(3) not null,
year int not null,
unemployment float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table internet_users (
iso3 char(3) not null,
year int not null,
internet_users float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table literacy_rate (
iso3 char(3) not null,
year int not null,
literacy_rate float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table asylum_seekers (
iso3 char(3) not null,
year int not null,
asylum_seekers float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table net_migration (
iso3 char(3) not null,
year int not null,
net_migration float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

create table university_enrollment (
iso3 char(3) not null,
year int not null,
university_enrollment float not null,
primary key (iso3, year),
foreign key (iso3) references countries (iso3)
);

SELECT
    column_name,
    data_type,
    character_maximum_length
FROM information_schema.columns
WHERE table_name = 'countries';