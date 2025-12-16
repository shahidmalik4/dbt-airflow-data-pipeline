## End-to-End Analytics Engineering Platform  

[![Python](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009485?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Metabase](https://img.shields.io/badge/Metabase-EC4A3F?style=for-the-badge&logo=metabase&logoColor=white)](https://www.metabase.com/)

[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue?style=for-the-badge)](https://github.com/yourusername/yourrepo/releases)
[![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)](https://github.com/yourusername/yourrepo/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=for-the-badge)](https://github.com/yourusername/yourrepo)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/yourusername/yourrepo?style=for-the-badge)](https://github.com/yourusername/yourrepo)



A **production-style analytics engineering project** that demonstrates how raw data moves from ingestion → transformation → orchestration → APIs → BI dashboards using modern data stack tools.

This project is designed to **mirror real-world data platforms** used by Analytics Engineers, Data Engineers, and BI teams.

---

## 🧠 Project Overview

This repository implements a **complete analytics workflow**:

1. **Data Ingestion** – Load TPCH-style data into Postgres  
2. **Transformations (dbt)** – Build staging, marts, and analytics models  
3. **Orchestration (Airflow)** – Schedule ingestion and dbt runs  
4. **Serving Layer (FastAPI)** – Expose analytics KPIs via REST APIs  
5. **BI & Dashboards (Metabase)** – Explore data visually  

The result is a **fully containerized analytics platform** you can run locally.

---

## 🧠 Skills Demonstrated

- Analytics Engineering best practices
- Data modeling (facts, dimensions, KPIs)
- dbt testing & documentation
- Workflow orchestration with Airflow
- API-driven analytics delivery
- BI enablement with Metabase
- Docker-based local data platforms

---

## 🏗️ File Structure
```
├── dags
│   └── my_dag.py
├── dbt
│   └── dbt_project
│       ├── analyses
│       ├── dbt_project.yml
│       ├── logs
│       │   └── dbt.log
│       ├── macros
│       │   └── generate_schema_name.sql
│       ├── models
│       │   ├── analytics
│       │   │   ├── avg_order_value.sql
│       │   │   ├── customer_cohort_retention.sql
│       │   │   ├── customer_ltv.sql
│       │   │   ├── daily_sales.sql
│       │   │   ├── order_fulfillment_efficiency.sql
│       │   │   ├── orders_over_time.sql
│       │   │   ├── product_profitability.sql
│       │   │   ├── regional_sales_performance.sql
│       │   │   ├── revenue_by_region.sql
│       │   │   ├── schema.yml
│       │   │   ├── supplier_performance_metrics.sql
│       │   │   ├── top_customers.sql
│       │   │   └── top_products.sql
│       │   ├── marts
│       │   │   ├── dims
│       │   │   │   ├── dim_customer.sql
│       │   │   │   ├── dim_part.sql
│       │   │   │   ├── dim_partsupp.sql
│       │   │   │   └── dim_supplier.sql
│       │   │   ├── facts
│       │   │   │   ├── fact_lineitem.sql
│       │   │   │   └── fact_orders.sql
│       │   │   └── schema.yml
│       │   └── staging
│       │       ├── schema.yml
│       │       ├── sources.yml
│       │       ├── stg_customers.sql
│       │       ├── stg_lineitems.sql
│       │       ├── stg_nation.sql
│       │       ├── stg_orders.sql
│       │       ├── stg_part.sql
│       │       ├── stg_partsupp.sql
│       │       ├── stg_region.sql
│       │       └── stg_supplier.sql
│       ├── profiles.yml
│       ├── README.md
│       ├── seeds
│       ├── snapshots
│       └── tests
├── docker-compose.yml
├── Dockerfile
├── fastapi
│   ├── analytics_api.log
│   ├── app
│   │   ├── main.py
│   │   ├── routers
│   │   │   ├── dbt_metadata.py
│   │   │   ├── dims_router.py
│   │   │   ├── facts_router.py
│   │   │   ├── __init__.py
│   │   │   └── kpis_router.py
│   │   ├── schemas
│   │   │   ├── analytics.py
│   │   │   ├── dbt.py
│   │   │   ├── dimensions.py
│   │   │   ├── facts.py
│   │   │   └── __init__.py
│   │   └── utils
│   │       ├── db.py
│   │       ├── __init__.py
│   │       └── logging.py
│   ├── Dockerfile
│   └── requirements.txt
├── include
│   ├── dashboard.png
│   └── fastapi.png
├── info.txt
├── ingestion
│   ├── __init__.py
│   ├── load_faker_data.py
│   └── postgres_data_load.py
├── README.md
├── requirements.txt
├── setup_project.sh
├── sql-scripts
│   ├── init-airflow.sql
│   └── init-warehouse.sql
├── start_services.sh
└── TPCH
    ├── customer.tbl
    ├── lineitem.tbl
    ├── nation.tbl
    ├── orders.tbl
    ├── partsupp.tbl
    ├── part.tbl
    ├── region.tbl
    └── supplier.tbl

```
---

## 🔧 Tech Stack

| Layer            | Tool |
|------------------|------|
| Database         | PostgreSQL |
| Transformations  | dbt |
| Orchestration    | Apache Airflow |
| API Layer        | FastAPI |
| BI / Dashboards  | Metabase |
| Containerization | Docker & Docker Compose |

---

## 📊 dbt Features Used
- Staging → Marts → Analytics layers
- Tests & custom tests
- Incremental models
- SCD snapshots
- Documentation generation

---

## ⏱️ Airflow Orchestration

Airflow orchestrates the entire pipeline:

- Warehouse readiness checks
- Ingestion tasks
- dbt run & dbt test
- Retry handling and logging

Each step is **modular, observable, and production-aligned**.

---

## Getting Started / Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/shahidmalik4/dbt-airflow-data-pipeline.git
cd dbt-airflow-data-pipeline
```

2. **Set up the Python environment**
```
python -m venv venv
source venv/bin/activate
.\venv\Scripts\Activate.ps1 (on windows - powershell)
.\venv\Scripts\activate.bat (on windows - command prompt)
```

3. **Make scripts executable (Linux / macOS only)**
```
chmod +x ./setup_project.sh
chmod +x ./start_services.sh
```

4. **Run Services (will pull all docker images, build, and run the containers required for the project)**
```
./setup_project.sh
```

5. **dbt Commands (Inside airflow-webserver Container)**
```
dbt debug
dbt docs generate
```

---

## 🌐 Access Services

| Service  | URL                        |
|----------|----------------------------|
| Airflow  | [http://localhost:8080](http://localhost:8080) |
| DBT Docs  | [http://localhost:8081](http://localhost:8081) |
| FastAPI  | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Metabase | [http://localhost:3000](http://localhost:3000) |

---

# FastAPI Swagger UI
![My Image](include/fastapi.png)


# Metabase Dashboard
![My Image](include/dashboard.png)


