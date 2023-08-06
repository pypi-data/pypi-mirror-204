"""OIDC Client exceptions."""


class ProviderConfigError(ValueError):
    """Raised when a ProviderConfig is invalid."""

    pass


class TokenRequestParamError(ValueError):
    """Raised when a bad param is provided to the token request helper."""

    pass


class AuthorizationError(RuntimeError):
    """Raised when the OAuth 2.1 authorization flow fails."""

    pass


class RedirectionError(AuthorizationError):
    """Raised when the OAuth 2.1 code redirect fails."""

    pass
