"""Authentication router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.core.security import create_access_token, hash_password, verify_password
from backend.app.models.organization import Membership, Organization
from backend.app.models.user import User
from backend.app.schemas.auth import (
    InviteStaffRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new catering organization and owner account."""
    existing_user = db.query(User).filter(User.email == req.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    # 1. Create Organization
    org = Organization(name=req.organization_name)
    db.add(org)
    db.flush()

    # 2. Create User
    user = User(
        email=req.email.lower(),
        password_hash=hash_password(req.password),
        full_name=req.full_name,
        is_active=True,
    )
    db.add(user)
    db.flush()

    # 3. Create Membership as Owner
    membership = Membership(
        user_id=user.id,
        organization_id=org.id,
        role="owner",
    )
    db.add(membership)
    db.commit()

    token = create_access_token(
        subject=user.id,
        organization_id=org.id,
        role="owner",
    )

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        organization_id=org.id,
        organization_name=org.name,
        role="owner",
        full_name=user.full_name,
        email=user.email,
    )


@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with email and password."""
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    # Get primary membership
    membership = db.query(Membership).filter(Membership.user_id == user.id).first()
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not belong to any organization.",
        )

    org = db.query(Organization).filter(Organization.id == membership.organization_id).first()
    org_name = org.name if org else "CaterIQ"

    token = create_access_token(
        subject=user.id,
        organization_id=membership.organization_id,
        role=membership.role,
    )

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        organization_id=membership.organization_id,
        organization_name=org_name,
        role=membership.role,
        full_name=user.full_name,
        email=user.email,
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Retrieve details for currently authenticated user."""
    user = db.query(User).filter(User.id == ctx.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/invite", status_code=status.HTTP_201_CREATED)
def invite_staff(
    req: InviteStaffRequest,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Invite or register staff member for the current organization."""
    existing_user = db.query(User).filter(User.email == req.email.lower()).first()
    if existing_user:
        # Check if already a member of this org
        existing_mem = (
            db.query(Membership)
            .filter(
                Membership.user_id == existing_user.id,
                Membership.organization_id == ctx.organization_id,
            )
            .first()
        )
        if existing_mem:
            raise HTTPException(status_code=400, detail="User is already a member of this organization.")
        target_user = existing_user
    else:
        target_user = User(
            email=req.email.lower(),
            password_hash=hash_password(req.password),
            full_name=req.full_name,
            is_active=True,
        )
        db.add(target_user)
        db.flush()

    membership = Membership(
        user_id=target_user.id,
        organization_id=ctx.organization_id,
        role=req.role,
        location_id=req.location_id,
    )
    db.add(membership)
    db.commit()

    return {"message": f"Successfully added {req.full_name} as {req.role}."}
