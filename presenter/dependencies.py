from typing import Annotated, AsyncGenerator
from redis.asyncio import Redis
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
from infrastructure.common.services.redis import RedisService
from infrastructure.common.services.user_id_by_referral_code import (
    RedisUserIDByReferralCodeService,
)
from infrastructure.sql.repos.referral_code import SQLReferralCodeRepository
from infrastructure.sql.repos.refresh_token import SQLRefreshTokenRepository
from infrastructure.sql.repos.user import SQLUserRepository
from infrastructure.sql.services.db import SQLDatabaseService
from presenter.services.jwt import JwtService, JwtSettings
from settings.db import DBSettings
from settings.redis import RedisSettings


async def get_session() -> AsyncGenerator[AsyncSession]:
    session = SQLDatabaseService.get(DBSettings())  # type: ignore
    async with session.begin():
        yield session


async def get_redis() -> Redis:
    return RedisService.get(RedisSettings())  # type: ignore


GetSession = Annotated[AsyncSession, Depends(get_session)]
GetRedis = Annotated[Redis, Depends(get_redis)]


def get_register_use_case(session: GetSession, redis: GetRedis) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        SQLUserRepository(session),
        SQLRefreshTokenRepository(session),
        RedisUserIDByReferralCodeService(
            SQLReferralCodeRepository(session),
            redis,
            RedisSettings(),  # type: ignore
        ),
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


def get_referrals_by_referrer_id_use_case(
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
