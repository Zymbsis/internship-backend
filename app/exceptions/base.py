from starlette import status


class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error"

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Forbidden"


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Resource not found"
