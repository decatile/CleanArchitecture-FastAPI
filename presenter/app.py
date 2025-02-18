from fastapi import FastAPI, HTTPException

from application.exceptions.base import ApplicationException

from .routes.auth import auth_router
from .routes.referral_codes import referral_codes_router

app = FastAPI()


@app.exception_handler(ApplicationException)
def application_exception_handler(exc: ApplicationException):
    raise HTTPException(400, str(exc))


app.include_router(auth_router)
app.include_router(referral_codes_router)
