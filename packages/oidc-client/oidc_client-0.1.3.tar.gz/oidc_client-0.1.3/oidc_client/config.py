"""Configuration utilities."""
import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .error import ProviderConfigError

# FIXME: type-check when we drop support for Python 3.10
try:
    import tomllib
except ImportError:
    import toml as tomllib  # type: ignore

DEFAULT_CONFIG_FILE = "pyproject.toml"

DEFAULT_OIDC_SCOPE = "openid profile email"
DEFAULT_REDIRECT_URI = "http://127.0.0.1:39303/oauth2/callback"


@dataclass(frozen=True)
class ProviderConfig:
    """OIDC provider configuration."""

    issuer: str
    authorization_endpoint: str
    token_endpoint: str


def validate_redirect_uri(uri: str) -> None:
    """Validate redirection URI."""
    redirect_uri = urlparse(uri)

    if redirect_uri.scheme not in ("http", "https"):
        raise ProviderConfigError("redirect scheme must be 'http' or 'https'.")

    if not redirect_uri.hostname or not redirect_uri.port:
        raise ProviderConfigError("redirection URI must include hostname and port.")

    if redirect_uri.params or redirect_uri.query:
        raise ProviderConfigError("redirection URI must not include query params.")

    if redirect_uri.hostname != "127.0.0.1" and redirect_uri.scheme == "http":
        raise ProviderConfigError("TLS must be enabled for non-loopback interfaces.")


@dataclass(frozen=True)
class ClientProfile:
    """OIDC client profile."""

    issuer: str
    client_id: str
    client_secret: str | None = None
    redirect_uri: str = DEFAULT_REDIRECT_URI
    scope: str = DEFAULT_OIDC_SCOPE

    def __post_init__(self) -> None:
        if not self.issuer.startswith("https://"):
            raise ProviderConfigError("OIDC issuer must be HTTPS.")

        validate_redirect_uri(self.redirect_uri)


def read_profile(
    path: Path,
    profile_name: str | None = None,
    overrides: argparse.Namespace | None = None,
) -> ClientProfile:
    """Read an (optionally named) OIDC client profile from a config file."""
    data = {}
    try:
        with open(path) as config_file:
            data = tomllib.loads(config_file.read())["tool"]["oidc"]
            if profile_name:
                data = data[profile_name]
    except FileNotFoundError:
        pass

    overrides = overrides or argparse.Namespace()

    issuer = (
        getattr(overrides, "issuer", None)
        or os.getenv("OIDC_ISSUER")
        or data.get("issuer")
    )
    client_id = (
        getattr(overrides, "client_id", None)
        or os.getenv("OIDC_CLIENT_ID")
        or data.get("client_id")
    )
    if not issuer or not client_id:
        raise ProviderConfigError(
            "An OIDC client valid profile requires at least the issuer and client ID "
            "to be set. Profile is built from args, env. vars, config file "
            "in this order."
        )

    stdin_secret = ""
    if getattr(overrides, "client_secret_stdin", False) and getattr(
        overrides, "stdin", None
    ):
        stdin_secret = overrides.stdin.readline().strip()

    return ClientProfile(
        issuer,
        client_id,
        client_secret=stdin_secret
        or os.getenv("OIDC_CLIENT_SECRET")
        or data.get("client_secret"),
        redirect_uri=getattr(overrides, "redirect_uri", None)
        or os.getenv("OIDC_REDIRECT_URI")
        or data.get("redirect_uri")
        or DEFAULT_REDIRECT_URI,
        scope=" ".join(getattr(overrides, "scope", []))
        or os.getenv("OIDC_SCOPE")
        or data.get("scope")
        or DEFAULT_OIDC_SCOPE,
    )
