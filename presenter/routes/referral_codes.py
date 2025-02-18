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
    get_referrals_by_referrer_id_use_ase,
)
from presenter.schemes.create_referral_response import CreateReferralResponse
from presenter.schemes.referral_code_create_request import ReferralCodeCreateRequest

referral_codes_router = APIRouter(prefix="/referral_codes")


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
    usecase: Annotated[GetReferralsByReferrerIDUseCase, Depends(get_referrals_by_referrer_id_use_ase)],
) -> list[int]:
    return await usecase.run(user_id.value)
