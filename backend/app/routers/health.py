from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "Stratège API"}


@router.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Stratège", "docs": "/docs"}
