from etl.extract.population import extract_population
from etl.transform.population import transform_population
from etl.load.population import load_population
from etl.extract.gdp import extract_gdp
from etl.transform.gdp import transform_gdp
from etl.load.gdp import load_gdp
from etl.extract.life_expectancy import extract_life_expectancy
from etl.transform.life_expectancy import transform_life_expectancy
from etl.load.life_expectancy import load_life_expectancy
from etl.extract.surface_area import extract_surface_area
from etl.transform.surface_area import transform_surface_area
from etl.load.surface_area import load_surface_area
from etl.extract.urban_population import extract_urban_population
from etl.transform.urban_population import transform_urban_population
from etl.load.urban_population import load_urban_population
from etl.extract.inflation import extract_inflation
from etl.transform.inflation import transform_inflation
from etl.load.inflation import load_inflation
from etl.extract.intentional_homcides import extract_intentional_homicides
from etl.transform.intentional_homcides import transform_intentional_homicides
from etl.load.intentional_homcides import load_intentional_homicides
from etl.extract.unemployment import extract_unemployment
from etl.transform.unemployment import transform_unemployment
from etl.load.unemployment import load_unemployment
from etl.extract.internet_users import extract_internet_users
from etl.transform.internet_users import transform_internet_users
from etl.load.internet_users import load_internet_users
from etl.extract.literacy_rate import extract_literacy_rate
from etl.transform.literacy_rate import transform_literacy_rate
from etl.load.literacy_rate import load_literacy_rate
from etl.extract.university_enrollment import extract_university_enrollment
from etl.transform.university_enrollment import transform_university_enrollment
from etl.load.university_enrollment import load_university_enrollment
from etl.extract.net_migration import extract_net_migration
from etl.transform.net_migration import transform_net_migration
from etl.load.net_migration import load_net_migration
from etl.extract.asylum_seekers import extract_asylum_seekers
from etl.transform.asylum_seekers import transform_asylum_seekers
from etl.load.asylum_seekers import load_asylum_seekers
from etl.extract.countries import extract_countries
from etl.transform.countries import transform_countries
from etl.load.countries import load_countries

def main():
    print("Starting GeoArchive pipeline...")

    print("Extracting")
    extract_population()
    extract_gdp()
    extract_life_expectancy()
    extract_surface_area()
    extract_urban_population()
    extract_inflation()
    extract_intentional_homicides()
    extract_unemployment()
    extract_internet_users()
    extract_literacy_rate()
    extract_university_enrollment()
    extract_net_migration()
    extract_asylum_seekers()
    extract_countries()

    print("Transforming")
    transform_population()
    transform_gdp()
    transform_life_expectancy()
    transform_surface_area()
    transform_urban_population()
    transform_inflation()
    transform_intentional_homicides()
    transform_unemployment()
    transform_internet_users()
    transform_literacy_rate()
    transform_university_enrollment()
    transform_net_migration()
    transform_asylum_seekers()
    transform_countries()

    print("Loading")
    load_population()
    load_gdp()
    load_life_expectancy()
    load_surface_area()
    load_urban_population()
    load_inflation()
    load_intentional_homicides()
    load_unemployment()
    load_internet_users()
    load_literacy_rate()
    load_university_enrollment()
    load_net_migration()
    load_asylum_seekers()
    load_countries()

    print("Pipeline finished successfully!")

if __name__ == "__main__":
    main()