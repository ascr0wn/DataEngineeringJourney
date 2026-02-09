import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import time
import os
import psycopg

USER = 'user'
PASSWORD = 'pass'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'my_db'
TABLE_NAME = 'yellow_taxi_data'
FILE_PATH = './taxi_data.parquet'
DB_CONNECTION = f'postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}' #establishing connection to the PostgreSQL database with Database URI (Uniform Resource Identifier)
BATCH_SIZE = 100000

def ingestion():
    if not os.path.exists(FILE_PATH):
        print(f"Error: File '{FILE_PATH}' not found in the current directory.")
        return

    start_time = time.time()

    try:
        ENGINE = create_engine(DB_CONNECTION)
        ENGINE.connect() # Testing the connection
        print("Database connection successful.")
    except Exception as e:
        print(f"Connection failed! Make sure Docker container is running and all dependencies are installed!\nError: {e}")
        return

    # print(f"Loading {FILE_PATH} into pandas.")
    # df = pd.read_parquet(FILE_PATH, ENGINE='pyarrow') #Since pandas cannot read parquet, we used external library pyarrow to read the parquet file.
    # df.columns = [col.lower().replace(' ', '_') for col in df.columns] #Converting all column names to lowercase for consistency (Postgres likes this!)
    # df['passenger_count'] = df['passenger_count'].fillna(0).astype('int32') #Handling missing values and optimizing data types (before it was float)
    # print(f"Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    #NOT USING THIS APPROACH AS THIS GETS THE FULL FILE IN MEMORY AT ONCE AND CAN CAUSE PROBLEMS

    #OR

    parquet_file = pq.ParquetFile(FILE_PATH) # This is just a pointer to the file, not reading the entire file now. {LAZY LOAD}
    parquet_iter = parquet_file.iter_batches(batch_size=BATCH_SIZE) #Ingest the file in chunks.
    is_first_batch = True
    total_rows = 0

    for batch in parquet_iter:
        df_batch = batch.to_pandas() # Converting since .to_sql() is only available for pandas DataFrames.
        df_batch.columns = [col.lower().replace(' ', '_') for col in df_batch.columns] #Converting all column names to lowercase for consistency (Postgres likes this!)
        df_batch['passenger_count'] = df_batch['passenger_count'].fillna(0).astype('int32') #Handling missing values and optimizing data types (example!)

        if is_first_batch:
            df_batch.to_sql(name=TABLE_NAME, con=ENGINE, if_exists='replace', index=False) #Creating a new table for the first batch. don't want dataframes index in database.
            is_first_batch = False

        else:
            df_batch.to_sql(name=TABLE_NAME, con=ENGINE, if_exists='append', index=False)
        total_rows += len(df_batch)
        print(f"Ingested {total_rows} rows so far...\n")
    end_time = time.time()
    duration = end_time - start_time
    print(f"Data ingestion completed in {duration:.2f} seconds.")

if __name__ == "__main__":
    ingestion()
