from etl.extract.population import extract_population
from etl.transform.population import transform_population
from etl.load.population import load_population
from etl.extract.gdp import extract_gdp
from etl.transform.gdp import transform_gdp
from etl.load.gdp import load_gdp
from etl.extract.life_expectancy import extract_life_expectancy
from etl.transform.life_expectancy import transform_life_expectancy
from etl.load.life_expectancy import load_life_expectancy

def main():
    print("Starting GeoArchive pipeline...")

    print("Extracting")
    extract_population()
    extract_gdp()
    extract_life_expectancy()

    print("Transforming")
    transform_population()
    transform_gdp()
    transform_life_expectancy()

    print("Loading")
    load_population()
    load_gdp()
    load_life_expectancy()

    print("Pipeline finished successfully!")

if __name__ == "__main__":
    main()