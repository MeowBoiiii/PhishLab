from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Template
from app.schemas.template import TemplateResponse

router = APIRouter()

@router.get("/", response_model=List[TemplateResponse], summary="Pobierz listę szablonów phishingowych")
def list_templates(db: Session = Depends(get_db)):
    """Zwraca listę wszystkich dostępnych szablonów ataków dla kreatora kampanii."""
    return db.query(Template).all()

@router.get("/{template_id}", response_model=TemplateResponse, summary="Pobierz pojedynczy szablon")
def get_template(template_id: int, db: Session = Depends(get_db)):
    """Pobiera szczegóły konkretnego szablonu na podstawie ID."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Szablon nie został znaleziony")
    return template