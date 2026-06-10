class AppError(Exception):
    message = "Internal server error"

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


class ForbiddenError(AppError):
    message = "Forbidden"


class NotFoundError(AppError):
    message = "Resource not found"


class ConflictError(AppError):
    message = "Conflict"
