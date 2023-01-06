from fastapi import HTTPException, status


class InternalError(HTTPException):
    CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Internal server error"

    def __init__(self, detail: str = None, **kwargs) -> None:
        detail = detail or self.DETAIL
        super().__init__(status_code=self.CODE, detail=detail, **kwargs)


class Unauthorized(InternalError):
    CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Not Authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class BadRequest(InternalError):
    CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class UnprocessableEntity(InternalError):
    CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    DETAIL = "Request could not be processed"


class NotFound(InternalError):
    CODE = status.HTTP_404_NOT_FOUND


class PermissionDenied(InternalError):
    CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class Conflict(InternalError):
    CODE = status.HTTP_409_CONFLICT
    DETAIL = "Conflict"
