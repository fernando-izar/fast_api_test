from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sql import SessionLocal
from sqlalchemy.orm import Session
from app.api.v1.routes_auth import get_current_user
from app.schemas.agent import AgentResponse, AgentCreate, AgentBase
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


@router.post("/", response_model=AgentResponse)
async def create_agent(db: db_dependency, user: user_dependency, payload: AgentCreate):
    agent = Agent(
        owner_id=user["id"],
        **payload.model_dump(),
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.get("/")
def list_agents(
    db: db_dependency,
    user: user_dependency,
):
    agents = db.query(Agent).filter(Agent.owner_id == user.get("id")).all()
    return agents
