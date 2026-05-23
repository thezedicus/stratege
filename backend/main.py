from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.routers import analysis, health
from app.database import create_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Stratège API...")
    await create_tables()  # no-op if DB unavailable — graceful degradation
    yield
    logger.info("Shutting down Stratège API.")


app = FastAPI(
    title="Stratège API",
    description="Expert virtuel en stratégie business, marketing et vente.",
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health.router, tags=["health"])
app.include_router(analysis.router, prefix="", tags=["analysis"])
