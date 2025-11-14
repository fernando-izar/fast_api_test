# app/db/nosql.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
mongo_db = client[settings.mongodb_db]
