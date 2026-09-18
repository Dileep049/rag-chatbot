from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from app.auth.security import verify_admin_credentials, create_access_token
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

@router.post("/login", response_model=LoginResponse)
async def login_endpoint(credentials: LoginRequest):
    """Authenticate Admin user and issue access token."""
    if not credentials.email or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password cannot be empty."
        )

    user_info = verify_admin_credentials(credentials.email, credentials.password)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token(user_info)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=user_info
    )

@router.get("/me")
async def get_me_endpoint(user: Dict[str, Any] = Depends(require_admin)):
    """Verify current token and return authenticated admin user info."""
    return {"user": user, "status": "authenticated"}
