# NYC Taxi Data Ingestion 🚖

This project ingests the NYC Yellow Taxi trip records (January 2025) into a local PostgreSQL database using Python and Docker.

**Source Data:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

---

## Prerequisites

* **Terminal:** Use a `bash` compatible terminal.
* **Docker:** Installed and running.
* **Tools:** `uv` is used for dependency management (inside containers).

---

## ⚡ Quick Start (The "Manual" Way)

If you want to run each container individually to understand how they connect.

### 1. Create a Docker network
```bash
docker network create taxi_net

```

### 2. Run PostgreSQL container

```bash
docker run -d \
  --name postgres_con \
  --network taxi_net \
  -p 5432:5432 \
  -e POSTGRES_USER="user" \
  -e POSTGRES_PASSWORD="pass" \
  -e POSTGRES_DB="taxi_data_db" \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:17-bookworm

```

### 3. Build the Ingestion Image

*Make sure `Dockerfile`, `pyproject.toml`, `uv.lock`, and `main.py` are in the current folder.*

```bash
docker build -t ingestion_script:1.0 .

```

### 4. Run the Ingestion Container

```bash
docker run -it --rm \
  --name ingestion_con \
  --network taxi_net \
  ingestion_script:1.0

```

---

## 🚀 The "Pro" Way (Docker Compose)

Instead of running commands manually, use Compose to spin up Postgres, pgAdmin, and the Ingestion container all at once.

### 1. Start everything

```bash
docker compose up -d --build

```

### 2. Enter the Ingestion Container

```bash
docker exec -it ingestion_con /bin/bash

```

### 3. Run the Script

Inside the container, run the script. **Crucial:** Override the host to point to the postgres container name.

```bash
uv run python main.py --pg-host postgres_con

```

---

## 🛠 CLI Arguments (Click)

The script uses `click` for robust CLI argument parsing. You can override any default configuration.

**View Help:**

```bash
uv run python main.py --help

```

**Full Custom Run Example:**

```bash
uv run python main.py \
  --pg-user user \
  --pg-pass pass \
  --pg-host postgres_con \
  --pg-port 5432 \
  --pg-db taxi_data_db \
  --year 2025 \
  --month 1 \
  --batchsize 100000

```

---

## 📊 Visualizing Data (pgAdmin)

If you used Docker Compose, pgAdmin is already running.

1. **Open Browser:** Go to [http://localhost:8085](https://www.google.com/search?q=http://localhost:8085)
2. **Login:**
* **Email:** `user@user.com`
* **Password:** `pass`


3. **Connect to Server:**
* Right-click **Servers** > **Register** > **Server**
* **General:** Name it `Taxi Docker DB`
* **Connection:**
* **Host:** `postgres_con` (Internal container name)
* **Username:** `user`
* **Password:** `pass`


* Click **Save**. Viola! 🎻



---

## 📝 Verification (SQL)

You can verify the data ingestion using `pgcli` from your local machine.

```bash
# Connect to localhost (since port 5432 is mapped)
uv run pgcli -h localhost -p 5432 -u user -d taxi_data_db

```

**Run a check:**

```sql
SELECT count(*) FROM yellow_taxi_data_2025_01;

```

---

## ⚠️ Notes for Local Development

If you are **not** using Docker and just want to run `main.py` on your laptop:

1. **Install `uv**`:
```bash
pip install uv

```


2. **Sync Dependencies**:
```bash
uv sync --frozen

```


3. **Run Script**:
```bash
# Note: Default host is 'localhost', so this works out of the box locally
uv run python main.py

```



```

```
