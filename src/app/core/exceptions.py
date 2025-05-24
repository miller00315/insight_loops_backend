from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException


class DomainException(Exception):
    """Base domain exception"""

    pass


class UserNotFoundException(DomainException):
    """Raised when user is not found"""

    pass


class UserAlreadyExistsException(DomainException):
    """Raised when user already exists"""

    pass


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "status_code": 422},
    )


async def domain_exception_handler(request: Request, exc: DomainException):
    if isinstance(exc, UserNotFoundException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, UserAlreadyExistsException):
        status_code = status.HTTP_409_CONFLICT
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc), "status_code": status_code},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(DomainException, domain_exception_handler)
