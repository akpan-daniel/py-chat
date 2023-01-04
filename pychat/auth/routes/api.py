from fastapi import APIRouter, Depends, HTTPException, status

from pychat.user.models import User
from pychat.user.schemas import input as user_input
from pychat.user.schemas import output as user_output

from .. import services
from ..schemas import input, output
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signin", response_model=output.LoginResponse)
async def signin(user_in: input.Signin):
    response_data = await services.signin_user(user_in)
    if response_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return response_data


@router.post("/signin/refresh", response_model=output.Tokens)
async def signin_refresh(token: input.RefreshToken):
    response_data = await services.signin_refresh(token.refresh)
    if not response_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
        )

    return response_data


@router.post("/signup", response_model=user_output.User)
async def signup(user_in: user_input.UserCreate):
    user = await services.signup_user(user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email taken already",
        )

    return user


@router.get(
    "/test-auth", response_model=user_output.User, status_code=status.HTTP_200_OK
)
async def test_auth(user: User = Depends(get_current_user)):
    return user
