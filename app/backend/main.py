from fastapi import FastAPI
from api.webhook import router as webhook_router
from etc.logging_config import setup_logging
from etc.middleware import RequestContextMiddleware

setup_logging()

app = FastAPI()

app.add_middleware(RequestContextMiddleware)    # ← СПОЧАТКУ

app.include_router(webhook_router)    # ← ПОТІМ

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
