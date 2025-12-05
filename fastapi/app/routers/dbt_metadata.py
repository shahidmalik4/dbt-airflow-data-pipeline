import json
import logging
from fastapi import APIRouter, HTTPException
from pathlib import Path
from datetime import datetime

router = APIRouter()

logger = logging.getLogger("dbt-metadata")

DBT_TARGET_PATH = Path(__file__).resolve().parents[3] / "dbt" / "dbt_project" / "target"


@router.get("/v1/dbt_metadata/", tags=["DBT"])
async def get_dbt_metadata():
    try:
        run_results_file = DBT_TARGET_PATH / "run_results.json"
        manifest_file = DBT_TARGET_PATH / "manifest.json"

        if not run_results_file.exists() or not manifest_file.exists():
            raise HTTPException(status_code=404, detail="DBT artifacts not found")

        with run_results_file.open("r") as f:
            run_results = json.load(f)

        with manifest_file.open("r") as f:
            manifest = json.load(f)

        freshness = {}
        raw_timestamp = run_results.get("metadata", {}).get("invocation_started_at", "unknown")
        try:
            last_run = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            last_run = raw_timestamp

        models_status = []
        for result in run_results.get("results", []):
            models_status.append({
                "unique_id": result.get("unique_id"),
                "status": result.get("status"),
                "execution_time": result.get("execution_time"),
            })

        response = {
            "last_run": last_run,
            "models_status": models_status,
            "manifest_summary": {
                "nodes": len(manifest.get("nodes", {})),
                "sources": len(manifest.get("sources", {}))
            },
            "freshness": freshness
        }

        logger.info("DBT metadata fetched successfully")
        return response

    except HTTPException as http_exc:
        logger.warning(f"HTTP error while fetching DBT metadata: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error fetching DBT metadata: {e}")

        raise HTTPException(status_code=500, detail="Internal Server Error reading DBT metadata")
