from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import task  # noqa: F401
from app.routers import task as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Creates database tables on startup.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Task Tracker API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router.router)


@app.get("/")
def read_root():
    return {"message": "Task Tracker API is running"}