from airflow.models.dag import DAG
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles.postgres import PostgresUserPasswordProfileMapping
from datetime import datetime
import os
from pathlib import Path

# Paths
DBT_PROJECT_PATH = Path("/opt/airflow/dbt/dbt_project")
DBT_EXECUTABLE_PATH = f"{os.getenv('AIRFLOW_HOME')}/dbt_venv/bin/dbt"
POSTGRES_CONN_ID = "postgres_local"

# Cosmos configs
_project_config = ProjectConfig(dbt_project_path=DBT_PROJECT_PATH)
_execution_config = ExecutionConfig(dbt_executable_path=DBT_EXECUTABLE_PATH)
profile_config = ProfileConfig(
    profile_name="dbt_project",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=POSTGRES_CONN_ID,
        profile_args={"schema": "staging", "dbname": "warehouse"},
    ),
)

# Define DAG
with DAG(
    dag_id="data_pipeline_dbt_etl",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["dbt", "cosmos"],
) as dag:

    # --- Staging TaskGroup ---
    staging_group = DbtTaskGroup(
        group_id="staging",
        project_config=_project_config,
        profile_config=profile_config,
        execution_config=_execution_config,
        default_args={"models": "staging.*"},
    )

    # --- Dim TaskGroup ---
    dims_group = DbtTaskGroup(
        group_id="dims",
        project_config=_project_config,
        profile_config=profile_config,
        execution_config=_execution_config,
        default_args={"select": "marts.dims.*"},
    )

    # --- Fact TaskGroup ---
    facts_group = DbtTaskGroup(
        group_id="facts",
        project_config=_project_config,
        profile_config=profile_config,
        execution_config=_execution_config,
        default_args={"select": "marts.facts.*"},
    )

    # --- Analytics TaskGroup ---
    analytics_group = DbtTaskGroup(
        group_id="analytics",
        project_config=_project_config,
        profile_config=profile_config,
        execution_config=_execution_config,
        default_args={"select": "analytics.*"},
    )

    # Set dependencies between TaskGroups
    chain(staging_group, dims_group, facts_group, analytics_group)
