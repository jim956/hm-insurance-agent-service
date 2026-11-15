from typing import Dict

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging,get_logger

from typing import Any

from contextlib import asynccontextmanager

configure_logging(settings.LOGGING_LEVEL)
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"【{settings.app.name}】应用启动中...")
    from app.infrastructure.database import check_database, close_database
    try:
        await check_database()
        yield
    finally:
        logger.info("应用关闭中... ")
        await close_database()

app = FastAPI(title=settings.app.name,debug=settings.app.debug,lifespan=lifespan)

@app.get("/healthy")
async def health_check()-> Dict[str, Any]:
    logger.info("health check被调用")
    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=False,
    )