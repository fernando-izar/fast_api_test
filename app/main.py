from fastapi import FastAPI
from app.api.v1.routes_jobs import router as jobs_router
from app.api.v1.routes_users import router as users_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_agent import router as agent_router
from app.api.v1.routes_job_logs import router as job_logs_router
from app.db.sql import Base, engine
from app.models.user import Users  # Import to register the model
from app.models.agent import Agent  # Import to register the model
from app.models.job import Job

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview API")

app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(agent_router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(job_logs_router, prefix="/api/v1/job_logs", tags=["job_logs"])
