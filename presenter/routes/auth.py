from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from application.usecases.auth_user import AuthUserUseCase
from application.usecases.register_user import RegisterUserUseCase
from presenter.dependencies import (
    JwtService,
    get_auth_use_case,
    get_jwt_service,
    get_register_use_case,
)
from presenter.schemes.auth_request import AuthRequest
from presenter.schemes.register_request import RegisterRequest
from presenter.schemes.tokens_response import TokensResponse
from presenter.schemes.tokens_set import TokensSet


def tokens_into_response(tokens: TokensSet) -> JSONResponse:
    resp = JSONResponse(
        {
            "access_token": tokens.access_token,
            "expires_in": tokens.access_token_expires_in,
        }
    )
    resp.set_cookie(
        "refresh_token",
        tokens.refresh_token,
        max_age=tokens.refresh_token_expires_in,
        secure=True,
        httponly=True,
    )
    return resp


auth_router = APIRouter()


@auth_router.post("/register", response_model=TokensResponse)
async def register(
    req: RegisterRequest,
    jwt: Annotated[JwtService, Depends(get_jwt_service)],
    usecase: Annotated[RegisterUserUseCase, get_register_use_case],
) -> JSONResponse:
    token = await usecase.run(req.referral_code, req.email, req.password)
    tokens = jwt.write(token)
    return tokens_into_response(tokens)


@auth_router.post("/auth", response_model=TokensResponse)
async def auth(
    req: AuthRequest,
    jwt: Annotated[JwtService, Depends(get_jwt_service)],
    usecase: Annotated[AuthUserUseCase, Depends(get_auth_use_case)],
) -> JSONResponse:
    token = await usecase.run(req.email, req.password)
    tokens = jwt.write(token)
    return tokens_into_response(tokens)
