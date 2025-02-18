from typing import Annotated

from pydantic import AfterValidator
from email_validator import validate_email as validate_email_base


def validate_email(value: str) -> str:
    validate_email_base(value)
    return value


Email = Annotated[str, AfterValidator(validate_email)]
