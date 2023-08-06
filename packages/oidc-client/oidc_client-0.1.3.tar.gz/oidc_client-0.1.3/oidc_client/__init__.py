from importlib import metadata

from .config import ProviderConfig
from .discovery import fetch_provider_config
from .error import (
    AuthorizationError,
    ProviderConfigError,
    RedirectionError,
    TokenRequestParamError,
)
from .lib import login
from .oauth import TokenResponse

__all__ = [
    "fetch_provider_config",
    "login",
    "TokenResponse",
    "ProviderConfig",
    "AuthorizationError",
    "ProviderConfigError",
    "RedirectionError",
    "TokenRequestParamError",
]
__version__ = metadata.version(__package__)
