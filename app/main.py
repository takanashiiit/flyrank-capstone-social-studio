from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import models  # noqa: F401 (registers the tables)
from app.database import create_db_and_tables
from app.routes_posts import router as posts_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(title="Social Media Studio", lifespan=lifespan)
app.include_router(posts_router)
@app.get("/health")
def health():
    return {"status": "ok"}

