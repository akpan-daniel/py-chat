from fastapi import APIRouter, Depends, status

from pychat.exceptions import Conflict, Unauthorized
from pychat.user.models import User
from pychat.user.schemas import input as user_input
from pychat.user.schemas import output as user_output

from .. import services
from ..schemas import input, output
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signin", status_code=status.HTTP_200_OK, response_model=output.LoginResponse
)
async def signin(user_in: input.Signin):
    response_data = await services.signin_user(user_in)
    if response_data is None:
        raise Unauthorized("Invalid credentials")

    return response_data


@router.post(
    "/signin/refresh", status_code=status.HTTP_200_OK, response_model=output.Tokens
)
async def signin_refresh(token: input.RefreshToken):
    response_data = await services.signin_refresh(token.refresh)
    if not response_data:
        raise Unauthorized("Token is invalid or expired")

    return response_data


@router.post("/logout", status_code=status.HTTP_205_RESET_CONTENT)
async def logout(user: User = Depends(get_current_user)):
    await services.delete_auth_token(user)


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=user_output.User
)
async def signup(user_in: user_input.UserCreate):
    user = await services.signup_user(user_in)
    if user is None:
        raise Conflict("Email taken already")

    return user


@router.get(
    "/test-auth", response_model=user_output.User, status_code=status.HTTP_200_OK
)
async def test_auth(user: User = Depends(get_current_user)):
    return user
