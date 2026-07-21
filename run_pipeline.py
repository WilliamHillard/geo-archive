from etl.extract.population import extract_population
from etl.transform.population import transform_population
from etl.load.population import load_population

def main():
    print("Starting GeoArchive pipeline...")

    print("Extracting population...")
    extract_population()

    print("Transforming population...")
    transform_population()

    print("Loading population...")
    load_population()

    print("Pipeline finished successfully!")

if __name__ == "__main__":
    main()