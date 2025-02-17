from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN
from application.usecases.auth_user import AuthUserUseCase
from application.usecases.create_referral_code import CreateReferralCodeUserCase
from application.usecases.delete_referral_code import DeleteReferralCodeUserCase
from application.usecases.get_referrals_by_referrer_id import (
    GetReferralsByReferrerIDUseCase,
)
from application.usecases.register_user import RegisterUserUseCase
from domain.entities.user import UserID
from presenter.services.jwt import JwtService, JwtSettings


def get_register_use_case() -> RegisterUserUseCase:
    raise NotImplementedError


def get_auth_use_case() -> AuthUserUseCase:
    raise NotImplementedError


def get_create_referral_code_use_case() -> CreateReferralCodeUserCase:
    raise NotImplementedError


def get_delete_referral_code_use_case() -> DeleteReferralCodeUserCase:
    raise NotImplementedError


def get_referrals_by_referrer_id_use_ase() -> GetReferralsByReferrerIDUseCase:
    raise NotImplementedError


def get_jwt_service() -> JwtService:
    return JwtService(JwtSettings())  # type: ignore


def get_current_user(
    jwt: Annotated[JwtService, Depends(get_jwt_service)],
    c: Annotated[HTTPAuthorizationCredentials, HTTPBearer()],
) -> UserID:
    if c.scheme != "Bearer":
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
    obj = jwt.read(c.credentials)
    if obj is None:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
    return UserID(obj.user_id)
