from fastapi import HTTPException
import logging
from databases import Database

logger = logging.getLogger("analytics-api")

DATABASE_URL = "postgresql://admin:admin@postgres_analytics:5432/warehouse"
database = Database(DATABASE_URL)

async def run_query(sql: str, params: dict = {}):
    try:
        logger.debug(f"Running SQL: {sql} | Params: {params}")
        return await database.fetch_all(query=sql, values=params)
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

