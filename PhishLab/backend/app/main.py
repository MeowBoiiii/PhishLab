from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.api.v1.endpoints import tracking

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="REST API dla platformy edukacyjnej PhishLab. Zawiera moduły autoryzacji, kampanii, trackingu i modułu edukacyjnego."
)

# Konfiguracja CORS (umożliwia frontendowi Maćka odpytywanie API z portu 5173/3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routery API v1
app.include_router(api_router, prefix=settings.API_V1_STR)

# Skrócone ścieżki do trackingu maili (np. /t/click/{token} lub /t/pixel/{token}.png)
app.include_router(tracking.router, prefix="/t", tags=["Tracking Public"])

@app.get("/health", tags=["Healthcheck"])
def health_check():
    """Prosty endpoint do sprawdzania, czy serwer żyje."""
    return {"status": "ok", "service": settings.PROJECT_NAME}

