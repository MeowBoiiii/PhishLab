from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Campaign
from app.schemas.campaign import CampaignCreate, CampaignResponse, DashboardStats

router = APIRouter()

@router.get("/dashboard-stats", response_model=DashboardStats, summary="Statystyki do Dashboardu")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Zwraca metryki bezpośrednio używane w widoku Dashboardu Maćka."""
    active_count = db.query(Campaign).filter(Campaign.status == "ACTIVE").count()
    
    # Wartości bazowe (w kolejnych sprintach zliczane dynamicznie z bazy)
    return {
        "risk_score": "Niski (24%)",
        "risk_score_value": 24,
        "active_campaigns": active_count,
        "clicks_last_7_days": 12
    }

@router.get("/", response_model=List[CampaignResponse], summary="Lista kampanii")
def list_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).offset(skip).limit(limit).all()
    return campaigns

@router.post("/", response_model=CampaignResponse, summary="Utworzenie nowej kampanii")
def create_campaign(campaign_in: CampaignCreate, db: Session = Depends(get_db)):
    campaign = Campaign(
        name=campaign_in.name,
        template_id=campaign_in.template_id,
        target_department=campaign_in.target_department,
        scheduled_at=campaign_in.scheduled_at,
        status="DRAFT"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

