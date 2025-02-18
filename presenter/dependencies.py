from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN
from application.usecases.auth_user import AuthUserUseCase, RefreshTokenSettings
from application.usecases.create_referral_code import CreateReferralCodeUserCase
from application.usecases.delete_referral_code import DeleteReferralCodeUserCase
from application.usecases.get_referrals_by_referrer_id import (
    GetReferralsByReferrerIDUseCase,
)
from application.usecases.register_user import RegisterUserUseCase
from domain.entities.user import UserID
from infrastructure.sql.repos.referral_code import SQLReferralCodeRepository
from infrastructure.sql.repos.refresh_token import SQLRefreshTokenRepository
from infrastructure.sql.repos.user import SQLUserRepository
from infrastructure.sql.services.db import SQLDatabaseService
from presenter.services.jwt import JwtService, JwtSettings
from settings.db import DBSettings


async def get_session() -> AsyncGenerator[AsyncSession]:
    session = SQLDatabaseService.session(DBSettings())  # type: ignore
    async with session.begin():
        yield session


GetSession = Annotated[AsyncSession, Depends(get_session)]


def get_register_use_case(session: GetSession) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        SQLUserRepository(session),
        SQLRefreshTokenRepository(session),
        SQLReferralCodeRepository(session),
        RefreshTokenSettings(),  # type: ignore
    )


def get_auth_use_case(session: GetSession) -> AuthUserUseCase:
    return AuthUserUseCase(
        SQLUserRepository(session),
        SQLRefreshTokenRepository(session),
        RefreshTokenSettings(),  # type: ignore
    )


def get_create_referral_code_use_case(
    session: GetSession,
) -> CreateReferralCodeUserCase:
    return CreateReferralCodeUserCase(
        SQLUserRepository(session), SQLReferralCodeRepository(session)
    )


def get_delete_referral_code_use_case(
    session: GetSession,
) -> DeleteReferralCodeUserCase:
    return DeleteReferralCodeUserCase(
        SQLUserRepository(session), SQLReferralCodeRepository(session)
    )


def get_referrals_by_referrer_id_use_ase(
    session: GetSession,
) -> GetReferralsByReferrerIDUseCase:
    return GetReferralsByReferrerIDUseCase(SQLUserRepository(session))


def get_jwt_service() -> JwtService:
    return JwtService(JwtSettings())  # type: ignore


def get_current_user(
    jwt: Annotated[JwtService, Depends(get_jwt_service)],
    c: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
) -> UserID:
    if c.scheme != "Bearer":
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
    obj = jwt.read(c.credentials)
    if obj is None:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
    return UserID(obj.user_id)
