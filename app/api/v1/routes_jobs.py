from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sql import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import Users
from app.schemas.user import UserVerification
from app.api.v1.routes_auth import get_current_user
from passlib.context import CryptContext
from app.schemas.job import JobBase, JobCreate, JobResponse, JobStatusUpdate
from app.models.job import Job
from app.models.agent import Agent


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


@router.post("/", response_model=JobResponse)
def create_job(
    payload: JobCreate,
    user: user_dependency,
    db: db_dependency,
):

    # Check if agent belongs to this user
    agent = (
        db.query(Agent)
        .filter(Agent.id == payload.agent_id, Agent.owner_id == user.get("id"))
        .first()
    )
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or not owned by user",
        )
    job = Job(
        **payload.model_dump(),
        user_id=user.get("id"),
        status="pending",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/")
async def list_jobs(
    user: user_dependency,
    db: db_dependency,
):

    jobs = db.query(Job).filter(Job.user_id == user.get("id")).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return jobs


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job(user: user_dependency, db: db_dependency, job_id: str):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    # Find the job and check if it belongs to the user
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.get("id")).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or you don't have permission to delete it",
        )

    # Delete the job
    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully", "job_id": str(job_id)}
