"""Custom exception hierarchy for Cloudability MCP Server."""


class CloudabilityError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(CloudabilityError):
    pass


class AuthorizationError(CloudabilityError):
    pass


class ValidationError(CloudabilityError):
    pass


class APIError(CloudabilityError):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: str | None = None,
        details: dict | None = None,
    ):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message, details)


class RateLimitError(APIError):
    pass


class NotFoundError(APIError):
    pass


class TimeoutError(CloudabilityError):
    pass


class ConfigurationError(CloudabilityError):
    pass
