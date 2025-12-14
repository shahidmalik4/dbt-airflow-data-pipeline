from pydantic import BaseModel
from typing import List

class DBTModelStatus(BaseModel):
    unique_id: str
    status: str
    execution_time: float

class DBTMetadata(BaseModel):
    last_run: str
    models_status: List[DBTModelStatus]
    manifest_summary: dict
    freshness: dict