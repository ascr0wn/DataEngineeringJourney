import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import time
import os
import psycopg
from tqdm.auto import tqdm
import fsspec
import click

@click.command()
@click.option('--pg-user', default='user', help='PostgreSQL user')
@click.option('--pg-pass', default='pass', help='PostgreSQL password')
@click.option('--pg-db', default='my_db', help='PostgreSQL database name')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--batchsize', default=100000, type=int, help='Chunk size for reading Parquet')

def postgres_parquet_ingestion(pg_user, pg_pass, pg_db, pg_host, pg_port, year, month, batchsize):
    file_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    db_connection = f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}' #establishing connection to the PostgreSQL database with Database URI (Uniform Resource Identifier)
    table_name = f"yellow-taxi-data{month}_{year}"
    start_time = time.time()
    try:
        engine = create_engine(db_connection)
        engine.connect() # Testing the connection
        print("Database connection successful.")
    except Exception as e:
        print(f"Connection failed! Make sure Docker container is running and all dependencies are installed!\nError: {e}")
        return

    # print(f"Loading {file_url} into pandas.")
    # df = pd.read_parquet(file_url, engine='pyarrow') #Since pandas cannot read parquet, we used external library pyarrow to read the parquet file.
    # df.columns = [col.lower().replace(' ', '_') for col in df.columns] #Converting all column names to lowercase for consistency (Postgres likes this!)
    # df['passenger_count'] = df['passenger_count'].fillna(0).astype('int32') #Handling missing values and optimizing data types (before it was float)
    # print(f"Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    #NOT USING THIS APPROACH AS THIS GETS THE FULL FILE IN MEMORY AT ONCE AND CAN CAUSE PROBLEMS
    #OR

    fs = fsspec.filesystem("https") # using fsspec with requests and aiohttp since pq donot work with pure url.
    parquet_file = pq.ParquetFile(file_url, filesystem=fs) #Just a pointer to the file for it's metadata, not loading it fully in memory. {LAZY LOAD}
    print(f"Metadata of the file is:\n {parquet_file.schema_arrow}")

    parquet_iter = parquet_file.iter_batches(batch_size=batchsize) #Ingest the file in chunks.
    is_first_batch = True
    total_rows = 0
    for batch in tqdm(parquet_iter):
        df_batch = batch.to_pandas() # Converting since .to_sql() is only available for pandas DataFrames.
        df_batch.columns = [col.lower().replace(' ', '_') for col in df_batch.columns] #Converting all column names to lowercase for consistency (Postgres likes this!)
        df_batch['passenger_count'] = df_batch['passenger_count'].fillna(0).astype('int32') #Handling missing values and optimizing data types (example!)
        if is_first_batch:
            df_batch.to_sql(name=table_name, con=engine, if_exists='replace', index=False) #Creating a new table for the first batch. don't want dataframes index in database.
            is_first_batch = False
        else:
            df_batch.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        total_rows += len(df_batch)
        print(f"Ingested {total_rows} rows so far...\n")
    end_time = time.time()
    duration = end_time - start_time
    print(f"Data ingestion of {total_rows} rows in local postgres database completed in {duration:.2f} seconds.")
if __name__ == "__main__":
    postgres_parquet_ingestion()
