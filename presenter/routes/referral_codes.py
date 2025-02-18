from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from application.usecases.create_referral_code import CreateReferralCodeUserCase
from application.usecases.delete_referral_code import DeleteReferralCodeUserCase
from application.usecases.get_referrals_by_referrer_id import (
    GetReferralsByReferrerIDUseCase,
)
from domain.entities.user import UserID
from presenter.dependencies import (
    get_create_referral_code_use_case,
    get_current_user,
    get_delete_referral_code_use_case,
)
from presenter.schemes.create_referral_response import CreateReferralResponse
from presenter.schemes.referral_code_create_request import ReferralCodeCreateRequest
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


referral_codes_router = APIRouter(prefix='/referral_codes')


@referral_codes_router.post("/create")
async def create(
    req: ReferralCodeCreateRequest,
    user_id: Annotated[UserID, Depends(get_current_user)],
    usecase: Annotated[
        CreateReferralCodeUserCase, Depends(get_create_referral_code_use_case)
    ],
) -> CreateReferralResponse:
    code = await usecase.run(user_id.value, req.expires_in)
    return CreateReferralResponse(code=code.code)


@referral_codes_router.get("/delete")
async def delete(
    user_id: Annotated[UserID, Depends(get_current_user)],
    usecase: Annotated[
        DeleteReferralCodeUserCase, Depends(get_delete_referral_code_use_case)
    ],
) -> JSONResponse:
    await usecase.run(user_id.value)
    return JSONResponse({})


@referral_codes_router.get("/referrals")
async def referrals(
    user_id: Annotated[UserID, Depends(get_current_user)],
    usecase: Annotated[GetReferralsByReferrerIDUseCase, Depends()],
) -> list[int]:
    return await usecase.run(user_id.value)
