from fastapi import FastAPI

from .routes.auth import auth_router
from .routes.referral_codes import referral_codes_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(referral_codes_router)
