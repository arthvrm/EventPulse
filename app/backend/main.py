import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from app.backend.api.webhook import router as webhook_router
from app.backend.db.database import create_tables
from app.backend.etc.logging_config import setup_logging
from app.backend.etc.middleware import RequestContextMiddleware

load_dotenv()
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await create_tables()
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestContextMiddleware)
app.include_router(webhook_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )