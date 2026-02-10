# NYC Taxi Data Ingestion 🚖

This project ingests the NYC Yellow Taxi trip records (January 2025) into a local PostgreSQL database using Python and Docker.

**Source Data:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

make sure you are in a bash terminal (commands here will be in bash, that's why) and follow below commands:

### 0. Create a Network
```bash
docker network create taxi-network

### 1. start a docker postgres container
```bash
docker run -it \
    --name postgres17 \
    -e POSTGRES_USER="user" \
    -e POSTGRES_PASSWORD="pass" \
    -e POSTGRES_DB="my_db" \
    -v my_db:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:17-trixie

(install uv before hand using pip install uv, and then 'uv venv' if not using the docker image method)

### 1.1 (optional) to interact with the database use pgcli
```bash
uv run pgcli -h localhost -u user -p 5432 -d my_db

## Notes: if not building docker image and just copying main.py from github, make sure to install dependency uv then use uv to install further dependencies like: pandas, psycopg, time, sqlalchemy, tqdm, os, pyarrow, fsspec, click, requests, aiohttp. (command: uv sync --frozen)

### 1.2 (optional) build your own ingestion docker image (not available at any remote docker image repo. build it yourself for the sake of practice)
docker build -t ingestion-script:1.0

### 1.3 docker run -it ingestion-script:1.0
here you are in /bin/bash in terminal, not python. you have to execute the main.py yourself.
this is because since main.py expects arguments from the cli (click python library).
format: docker run -it --rm \
    --network taxi-network \
    taxi-ingest:v1 \
    python main.py \

run uv run python main.py --help for more information.

format uv run main.py \
    --pg-user user \
    --pg-pass pass \
    --pg-host postgres-db \
    --pg-port 5432 \
    --pg-db my_db \
    --year 2025 \
    --month 1 \
    --batchsize 100000
use the above format to be specific with your choice. the given values in the example are also the default values for the arguments.
