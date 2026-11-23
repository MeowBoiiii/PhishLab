from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models import Admin
from app.schemas.auth import LoginRequest, TokenResponse, AdminResponse, AdminCreate

router = APIRouter()

security = HTTPBearer()

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """Weryfikuje token JWT z nagłówka Authorization: Bearer <token>."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nie można zweryfikować tożsamości",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        admin_id: str = payload.get("sub")
        if admin_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    if admin is None:
        raise credentials_exception
    return admin

@router.post("/login", response_model=TokenResponse, summary="Logowanie administratora")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Logowanie administratora za pomocą emaila i hasła."""
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

@router.get("/me", response_model=AdminResponse, summary="Pobierz dane zalogowanego administratora")
def get_me(current_admin: Admin = Depends(get_current_admin)):
    """Zwraca profil aktualnie uwierzytelnionego administratora na podstawie tokena JWT."""
    return current_admin
