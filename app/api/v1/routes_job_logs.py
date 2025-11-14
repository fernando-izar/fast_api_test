from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sql import SessionLocal
from sqlalchemy.orm import Session
from app.api.v1.routes_auth import get_current_user
from app.schemas.job_log import JobLogCreate, JobLogResponse
from app.db.mongo_job_logs import create_job_log, get_job_log_by_job_id
from uuid import UUID


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error to connect sql db",
        )
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=str)
async def create_log(user: db_dependency, payload: JobLogCreate):
    data = payload.model_dump()
    data["job_id"] = str(payload.job_id)

    inserted_id = await create_job_log(data)
    return inserted_id


@router.get("/{job_id}", response_model=JobLogResponse)
async def get_logs(job_id: UUID):
    doc = await get_job_log_by_job_id(job_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Job log not found")

    doc["job_id"] = UUID(doc["job_id"])
    doc.pop("_id", None)

    return doc
