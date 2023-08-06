"""High level OpenID Connect login helper."""
from .config import DEFAULT_OIDC_SCOPE, ProviderConfig
from .error import TokenRequestParamError
from .oauth import (
    GrantType,
    TokenResponse,
    fetch_token,
    handle_authorization_code,
    start_authorization_code_flow,
)
from .pkce import PKCESecret


def login(
    provider_config: ProviderConfig,
    client_id: str,
    client_secret: str | None = None,
    redirect_uri: str | None = None,
    scope: str = DEFAULT_OIDC_SCOPE,
    interactive: bool = False,
) -> TokenResponse:
    """Perform OIDC login.

    The interactive mode requires the user to log in using a web browser.
    """
    if interactive:
        if not redirect_uri:
            raise TokenRequestParamError(
                "redirect_uri must be provided for interactive login."
            )

        pkce_secret = PKCESecret()
        state = start_authorization_code_flow(
            provider_config.authorization_endpoint,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            pkce_secret=pkce_secret,
        )
        code = handle_authorization_code(state=state, redirect_uri=redirect_uri)
        return fetch_token(
            provider_config.token_endpoint,
            grant_type=GrantType.AUTHORIZATION_CODE,
            client_id=client_id,
            redirect_uri=redirect_uri,
            code=code,
            pkce_secret=pkce_secret,
        )

    if not client_secret:
        raise TokenRequestParamError(
            "client_secret must be provided for non-interactive login."
        )

    return fetch_token(
        provider_config.token_endpoint,
        grant_type=GrantType.CLIENT_CREDENTIALS,
        client_id=client_id,
        client_secret=client_secret,
    )
