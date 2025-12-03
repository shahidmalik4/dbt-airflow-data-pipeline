from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles.postgres import PostgresUserPasswordProfileMapping
from datetime import datetime
from pathlib import Path


DBT_PROJECT_PATH = Path("/opt/airflow/dbt/dbt_project")
POSTGRES_CONN_ID = "postgres_local"

_project_config = ProjectConfig(dbt_project_path=DBT_PROJECT_PATH)
profile_config = ProfileConfig(
    profile_name="dbt_project",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=POSTGRES_CONN_ID,
        profile_args={"dbname": "warehouse", "schema": "staging"},
    ),
)

dbt_project_dag = DbtDag(
    dag_id="data_pipeline_dbt_etl",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["dbt", "cosmos"],

    # Cosmos Dbt Arguments
    project_config=_project_config,
    profile_config=profile_config,
    
    # Default arguments
    default_args={
        "owner": "airflow",
        "retries": 1,
    },
    
)