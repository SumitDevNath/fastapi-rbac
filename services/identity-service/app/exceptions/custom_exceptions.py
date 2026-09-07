class AppException(Exception):

    def __init__(
        self,
        message: str,
        details=None,
    ):
        self.message = message
        self.details = details
        super().__init__(message)


class AuthenticationFailedError(
    AppException
):
    pass


class PermissionDeniedError(
    AppException
):
    pass


class ResourceConflictError(
    AppException
):
    pass