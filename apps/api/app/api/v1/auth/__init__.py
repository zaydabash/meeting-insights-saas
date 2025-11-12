from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.schemas.user import UserResponse
from app.schemas.organization import OrganizationResponse

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create organization
    org = Organization(name=request.org_name)
    db.add(org)
    db.flush()
    
    # Create user
    from app.models.user import UserRole
    user = User(
        org_id=org.id,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        role=UserRole.ADMIN,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.refresh(org)
    
    # Create token
    token = create_access_token(data={"sub": user.id, "org_id": user.org_id})
    
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(user),
        org=OrganizationResponse.model_validate(org),
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    org = db.query(Organization).filter(Organization.id == user.org_id).first()
    
    token = create_access_token(data={"sub": user.id, "org_id": user.org_id})
    
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(user),
        org=OrganizationResponse.model_validate(org),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse.model_validate(current_user)
