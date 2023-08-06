"""High level OpenID Connect configuration discovery helper."""
import json
from urllib.parse import urljoin
from urllib.request import urlopen

from .config import ProviderConfig
from .error import ProviderConfigError


def fetch_provider_config(issuer: str) -> ProviderConfig:
    """Fetch a provider configuration from an OIDC issuer (URL)."""
    if not issuer.startswith("https://"):
        raise ValueError("The issuer URL must be HTTPS.")

    with urlopen(urljoin(issuer, ".well-known/openid-configuration")) as response:
        data = json.load(response)

        if data["issuer"] != issuer:
            raise ProviderConfigError(
                "The issuer value returned must be identical to the issuer URL."
            )

        return ProviderConfig(
            issuer=issuer,
            authorization_endpoint=data["authorization_endpoint"],
            token_endpoint=data["token_endpoint"],
        )
