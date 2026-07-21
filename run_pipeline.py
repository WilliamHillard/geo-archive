from etl.extract.population import extract_population
from etl.transform.population import transform_population
from etl.load.population import load_population
from etl.extract.gdp import extract_gdp
from etl.transform.gdp import transform_gdp
from etl.load.gdp import load_gdp

def main():
    print("Starting GeoArchive pipeline...")

    print("Extracting")
    extract_population()
    extract_gdp()

    print("Transforming")
    transform_population()
    transform_gdp()

    print("Loading")
    load_population()
    load_gdp()

    print("Pipeline finished successfully!")

if __name__ == "__main__":
    main()