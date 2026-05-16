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
    await create_tables()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Stratège API",
    description="API pour l'expert virtuel en stratégie business, marketing et vente",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
