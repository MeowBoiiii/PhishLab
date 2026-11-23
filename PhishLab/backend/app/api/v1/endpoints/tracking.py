from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models import CampaignTracking

router = APIRouter()

# 1x1 przezroczysty piksel GIF
TRANSPARENT_PIXEL_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04"
    b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)

@router.get("/pixel/{tracking_token}.png", summary="Piksel śledzący otwarcie wiadomości email")
def track_email_open(tracking_token: str, db: Session = Depends(get_db)):
    """Rejestruje otwarcie maila przez pobranie niewidocznego obrazka."""
    tracking = db.query(CampaignTracking).filter(CampaignTracking.tracking_token == tracking_token).first()
    if tracking and not tracking.is_opened:
        tracking.is_opened = True
        db.commit()

    return Response(content=TRANSPARENT_PIXEL_GIF, media_type="image/gif")

@router.get("/click/{tracking_token}", summary="Kliknięcie w link phishingowy i przekierowanie")
def track_link_click(tracking_token: str, db: Session = Depends(get_db)):
    """Rejestruje kliknięcie użytkownika w fałszywy odnośnik i przekierowuje go na stronę edukacyjną."""
    tracking = db.query(CampaignTracking).filter(CampaignTracking.tracking_token == tracking_token).first()
    if tracking:
        if not tracking.is_clicked:
            tracking.is_clicked = True
            db.commit()

    # Przekierowanie na frontendową stronę edukacyjną (zgodnie z konfiguracją)
    frontend_edu_url = f"{settings.FRONTEND_URL}/education/caught?token={tracking_token}"
    return RedirectResponse(url=frontend_edu_url, status_code=302)

