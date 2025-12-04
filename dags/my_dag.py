import sys
from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles.postgres import PostgresUserPasswordProfileMapping

# Import your ingestion function
from ingestion.postgres_data_load import main as load_raw_data

# Add project root to Python path (if needed)
sys.path.append(str(Path(__file__).resolve().parent.parent))

# ---------------- DBT CONFIG ----------------
DBT_PROJECT_PATH = Path("/opt/airflow/dbt/dbt_project")
POSTGRES_CONN_ID = "postgres_local"

_project_config = ProjectConfig(dbt_project_path=DBT_PROJECT_PATH)
_profile_config = ProfileConfig(
    profile_name="dbt_project",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=POSTGRES_CONN_ID,
        profile_args={"dbname": "warehouse", "schema": "staging"},
    ),
)

# ---------------- DAG ----------------
with DAG(
    dag_id="full_tpch_dbt_pipeline",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["dbt", "tpch", "cosmos"],
) as dag:

    # 1) Load RAW TPCH data
    load_raw_task = PythonOperator(
        task_id="load_raw_data",
        python_callable=load_raw_data,
        retries=2,
        retry_delay=timedelta(minutes=5),
    )

    # 2) Run dbt models
    dbt_run = DbtTaskGroup(
        group_id="dbt_run",
        project_config=_project_config,
        profile_config=_profile_config,
    )


    load_raw_task >> dbt_run