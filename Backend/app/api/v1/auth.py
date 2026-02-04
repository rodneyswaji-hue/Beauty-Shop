from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core import security
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=security.Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db=Depends(security.get_db)):
    # check existing user
    existing = security.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed = security.get_password_hash(user_in.password)
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        phone=user_in.phone,
        address=user_in.address,
        hashed_password=hashed,
        is_Active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = security.create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=security.Token)
def login(credentials: LoginSchema, db=Depends(security.get_db)):
    user = security.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = security.create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(security.get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "address": current_user.address,
        "is_admin": bool(getattr(current_user, "is_Admin", False)),
        "is_active": bool(getattr(current_user, "is_Active", False)),
        "created_at": getattr(current_user, "created_at", None),
    }

@router.put("/profile", response_model=UserOut)
def update_profile(
    user_update: UserCreate,
    db=Depends(security.get_db),
    current_user: User = Depends(security.get_current_user)
):
    # Update user fields
    for key, value in user_update.dict(exclude_unset=True).items():
        if key == "password" and value:
            setattr(current_user, "hashed_password", security.get_password_hash(value))
        elif key != "password":
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "address": current_user.address,
        "is_admin": bool(getattr(current_user, "is_Admin", False)),
        "is_active": bool(getattr(current_user, "is_Active", False)),
        "created_at": getattr(current_user, "created_at", None),
    }
