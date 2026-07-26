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

def main():
    print("Starting GeoArchive pipeline...")

    print("Extracting")
    extract_population()
    extract_gdp()
    extract_life_expectancy()
    extract_surface_area()

    print("Transforming")
    transform_population()
    transform_gdp()
    transform_life_expectancy()
    transform_surface_area()

    print("Loading")
    load_population()
    load_gdp()
    load_life_expectancy()
    load_surface_area()

    print("Pipeline finished successfully!")

if __name__ == "__main__":
    main()