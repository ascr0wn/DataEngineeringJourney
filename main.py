import pandas as pd

def main():
    print("Hello from dataengineeringjourney!")
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"
    taxi_data = pd.read_parquet(url)
    print(taxi_data.head())

if __name__ == "__main__":
    main()
