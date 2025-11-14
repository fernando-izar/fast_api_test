from typing import Optional, Dict, Any
from uuid import UUID

from app.db.nosql import mongo_db

collection = mongo_db["job_logs"]


async def create_job_log(data: Dict[str, Any]) -> str:
    """
    data structure example:
    {
        "job_id": "uuid-string",
        "messages": [ {...}, {...} ]
    }
    """
    job_log = await collection.find_one({"job_id": data["job_id"]})

    if not job_log:
        result = await collection.insert_one(data)
        return str(result.inserted_id)

    else:
        # Add new messages to existing job log
        result = await collection.update_one(
            {"_id": job_log["_id"]},
            {"$push": {"messages": {"$each": data["messages"]}}},
        )
        return str(job_log["_id"])


async def get_job_log_by_job_id(job_id: UUID) -> Optional[Dict[str, Any]]:
    doc = await collection.find_one({"job_id": str(job_id)})
    if not doc:
        return None

    # normalize _id to string
    doc["_id"] = str(doc["_id"])
    return doc
