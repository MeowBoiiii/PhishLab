from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CampaignBase(BaseModel):
    name: str
    template_id: int
    target_department: str
    scheduled_at: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    id: int
    admin_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    risk_score: str
    risk_score_value: int
    active_campaigns: int
    clicks_last_7_days: int

