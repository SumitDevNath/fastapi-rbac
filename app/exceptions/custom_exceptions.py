from typing import Any, Optional


class AppException(Exception):
    """Base class for all application-level domain exceptions."""
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(message)


class ResourceNotFoundError(AppException):
    """Raised when an entity is not found in the database."""
    def __init__(self, resource_name: str, identifier: Any):
        super().__init__(
            message=f"{resource_name} with identifier '{identifier}' was not found.",
            details={"resource": resource_name, "identifier": identifier}
        )


class ResourceConflictError(AppException):
    """Raised when an entity cannot be created due to unique constraint collisions."""
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message=message, details=details)


class PermissionDeniedError(AppException):
    """Raised when a user lacks sufficient permissions for a domain action."""
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message=message)


class AuthenticationFailedError(AppException):
    """Raised when credential verification fails."""
    def __init__(self, message: str = "Invalid authentication credentials."):
        super().__init__(message=message)