from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.address.routes import router as address_router
from app.user.routes import router as user_router
from dotenv import load_dotenv
from app.logging.logging_config import setup_logging
from loguru import logger
import uvicorn
import os

load_dotenv()
setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Address Book API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    app.include_router(address_router)
    app.include_router(user_router)

    @app.get("/ping")
    def ping():
        logger.info("Ping endpoint called")
        return JSONResponse(content={"message": "pong"})

    return app

app = create_app()

if __name__ == "__main__":
    logger.info("Starting Address Book API...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("RELOAD", False)),
        log_level=os.getenv("LOG_LEVEL", "info"),
    )