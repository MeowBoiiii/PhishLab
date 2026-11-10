from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models import Admin
from app.schemas.auth import LoginRequest, TokenResponse, AdminResponse, AdminCreate

router = APIRouter()

@router.post("/login", response_model=TokenResponse, summary="Logowanie administratora")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Logowanie administratora za pomocą emaila i hasła (pasuje do widoku Maćka)."""
    admin = db.query(Admin).filter(Admin.email == login_data.email).first()
    if not admin or not verify_password(login_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy adres email lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=admin.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=AdminResponse, summary="Rejestracja administratora (dev/seed)")
def register(admin_data: AdminCreate, db: Session = Depends(get_db)):
    """Tworzy nowego administratora (pomocne do przygotowania konta testowego)."""
    existing_user = db.query(Admin).filter(
        (Admin.email == admin_data.email) | (Admin.username == admin_data.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Użytkownik z tym mailem lub nazwą już istnieje")

    hashed_pw = get_password_hash(admin_data.password)
    new_admin = Admin(
        username=admin_data.username,
        email=admin_data.email,
        password_hash=hashed_pw
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

