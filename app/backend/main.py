import uvicorn
import sys
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from app.backend.api.webhook import router as webhook_router
from app.backend.etc.logging_config import setup_logging
from app.backend.etc.middleware import RequestContextMiddleware

load_dotenv()
setup_logging()


app = FastAPI()

app.add_middleware(RequestContextMiddleware)
app.include_router(webhook_router)


if __name__ == "__main__":
    if "--local" in sys.argv:
        uvicorn.run(
            "app.backend.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
    elif "--docker" in sys.argv:
        uvicorn.run(
            "app.backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
        )
    else:
        print("Choose command-line argument(--local or --docker).")