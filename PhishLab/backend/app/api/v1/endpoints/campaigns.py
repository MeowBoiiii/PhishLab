import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Campaign, Admin, TargetUser, CampaignTracking, Template
from app.schemas.campaign import CampaignCreate, CampaignResponse, DashboardStats
from app.api.v1.endpoints.auth import get_current_admin

router = APIRouter()


@router.get("/dashboard-stats", response_model=DashboardStats, summary="Statystyki do Dashboardu")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Zwraca metryki bezpośrednio używane w widoku Dashboardu Maćka."""
    active_count = db.query(Campaign).filter(Campaign.status == "ACTIVE").count()
    total_clicks = db.query(CampaignTracking).filter(CampaignTracking.is_clicked == True).count()
    total_sent = db.query(CampaignTracking).count()

    if total_sent > 0:
        risk_value = int(round((total_clicks / total_sent) * 100))
        if risk_value < 20:
            risk_label = f"Niski ({risk_value}%)"
        elif risk_value < 50:
            risk_label = f"Średni ({risk_value}%)"
        else:
            risk_label = f"Wysoki ({risk_value}%)"
    else:
        risk_value = 0
        risk_label = "Brak danych (0%)"

    return {
        "risk_score": risk_label,
        "risk_score_value": risk_value,
        "active_campaigns": active_count,
        "clicks_last_7_days": total_clicks
    }
@router.get("/", response_model=List[CampaignResponse], summary="Lista kampanii")
def list_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).offset(skip).limit(limit).all()
    return campaigns

@router.post("/", response_model=CampaignResponse, summary="Utworzenie nowej kampanii")
def create_campaign(
    campaign_in: CampaignCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Tworzy nową kampanię powiązaną z aktualnie zalogowanym administratorem."""
    # Opcjonalnie: sprawdzamy, czy szablon w ogóle istnieje
    template = db.query(Template).filter(Template.id == campaign_in.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Wybrany szablon nie istnieje")

    campaign = Campaign(
        name=campaign_in.name,
        template_id=campaign_in.template_id,
        target_department=campaign_in.target_department,
        scheduled_at=campaign_in.scheduled_at,
        admin_id=current_admin.id,  # <<< PRZYPISUJEMY ID ZALOGOWANEGO ADMINA
        status="DRAFT"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.get("/{campaign_id}", response_model=CampaignResponse, summary="Szczegóły kampanii")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Zwraca szczegóły konkretnej kampanii na podstawie jej ID."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Kampania nie została znaleziona")
    return campaign

@router.post("/{campaign_id}/launch", response_model=CampaignResponse, summary="Uruchomienie kampanii")
def launch_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Uruchamia kampanię:
    1. Zmienia status na ACTIVE.
    2. Szuka pracowników z danego działu (target_users).
    3. Generuje dla każdego pracownika unikalny tracking_token.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Kampania nie została znaleziona")

    if campaign.status == "ACTIVE":
        raise HTTPException(status_code=400, detail="Kampania jest już aktywna")

    # 1. Pobieramy użytkowników z grupy docelowej (lub wszystkich, jeśli dział = 'wszyscy')
    if campaign.target_department.lower() == "wszyscy":
        targets = db.query(TargetUser).all()
    else:
        targets = db.query(TargetUser).filter(
            TargetUser.department.ilike(campaign.target_department)
        ).all()

    # 2. Generujemy wpisy trackingowe dla każdego pracownika
    for user in targets:
        # Sprawdzamy, czy użytkownik nie ma już przypisanego tokena w tej kampanii
        existing = db.query(CampaignTracking).filter(
            CampaignTracking.campaign_id == campaign.id,
            CampaignTracking.user_id == user.id
        ).first()

        if not existing:
            token = uuid.uuid4().hex  # unikalny losowy hash, np. "9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d"
            tracking = CampaignTracking(
                campaign_id=campaign.id,
                user_id=user.id,
                tracking_token=token,
                is_opened=False,
                is_clicked=False
            )
            db.add(tracking)

    # 3. Aktywujemy kampanię
    campaign.status = "ACTIVE"
    db.commit()
    db.refresh(campaign)
    return campaign