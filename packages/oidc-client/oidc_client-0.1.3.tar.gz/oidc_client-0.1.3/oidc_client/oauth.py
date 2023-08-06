"""OAuth 2.1 authorization flow definition utilities."""
from __future__ import annotations

import base64
import json
import random
import string
import webbrowser
from dataclasses import dataclass, fields
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.resources import files
from typing import cast
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from .error import AuthorizationError, RedirectionError
from .pkce import PKCESecret
from .tls import setup_tls

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum  # type: ignore


class AuthorizationCodeHandler(BaseHTTPRequestHandler):
    """OAuth 2.1 authorization code flow (with PKCE) HTTP handler."""

    def __init__(
        self, request: bytes, client_address: tuple[str, int], server: RedirectionServer
    ):
        # Required for type-checking the server object
        super().__init__(request, client_address, server)

    def log_message(self, *_: str) -> None:
        # Silence HTTP server logging to *stdout* and *stderr*
        pass

    def do_GET(self) -> None:
        # BUG: init method accepts a 'RedirectionServer'
        # but it remains a 'BaseServer' here!
        server = cast(RedirectionServer, self.server)

        url = urlparse(self.path)

        # Ignore request to a path different from the specified redirection
        if url.path != server.redirection_path:
            self.send_error(HTTPStatus.NOT_FOUND, message="Not found")
            return

        qs = parse_qs(url.query)

        # Validate state
        try:
            (query_state,) = qs.get("state", [])
            if query_state != server.state:
                server.error = RedirectionError(
                    "bad state in OAuth redirect URI: "
                    f"'{query_state}', expected '{server.state}'."
                )
        except (TypeError, ValueError):
            server.error = RedirectionError("no state in OAuth redirect URI.")

        # Get code
        try:
            (server.code,) = qs.get("code", [])
        except (TypeError, ValueError):
            server.error = RedirectionError("no code in OAuth redirect URI.")

        # Send OK or error response
        if server.error:
            self.send_error(
                HTTPStatus.BAD_REQUEST, message=f"OAuth error: {server.error}"
            )
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Connection", "close")
        self.send_header("Content-type", "text/html;utf-8")
        self.end_headers()

        self.wfile.write(files(__package__).joinpath("index.html").read_bytes())


class RedirectionServer(HTTPServer):
    """OAuth 2.1 authorization code flow (with PKCE) HTTP server."""

    def __init__(
        self,
        server_address: tuple[str, int],
        handler_class: type[AuthorizationCodeHandler],
        redirection_path: str,
        state: str,
        tls: bool = False,
    ):
        super().__init__(server_address, handler_class)

        self.redirection_path = redirection_path or "/"
        self.state = state

        if tls:
            self.socket = setup_tls(self.socket)

        self.code: str | None = None
        self.error: AuthorizationError | None = None


def start_authorization_code_flow(
    endpoint: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    pkce_secret: PKCESecret,
) -> str:
    """Start OAuth 2.1 authorization code flow (with PKCE).

    Authorization code flow is interactive, this opens a web browser allowing a user to
    log in.
    """
    state = base64.urlsafe_b64encode(
        "".join(
            random.choices(string.ascii_letters + string.digits + "-._~", k=32)
        ).encode()
    )
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
        "scope": scope,
        "code_challenge": pkce_secret.challenge,
        "code_challenge_method": pkce_secret.challenge_method,
    }
    webbrowser.open(f"{endpoint}?{urlencode(params)}")
    return state.decode()


def handle_authorization_code(state: str, redirect_uri: str) -> str:
    """Serve local HTTP server to handle the OAuth 2.1 authorization code redirect."""
    server_conf = urlparse(redirect_uri)

    if not server_conf.hostname or not server_conf.port:
        raise ValueError("cannot start redirection server without hostname and port.")

    with RedirectionServer(
        (server_conf.hostname, server_conf.port),
        AuthorizationCodeHandler,
        redirection_path=server_conf.path,
        state=state,
        tls=server_conf.scheme == "https",
    ) as httpd:
        while not httpd.code and not httpd.error:
            httpd.handle_request()
        if httpd.error:
            raise httpd.error
        if not httpd.code:
            # This should not ever be reached.
            raise AuthorizationError(  # pragma: no cover
                "no authorization code, unknown error."
            )

    return httpd.code


class GrantType(StrEnum):
    """OAuth 2.1 authorization grant types."""

    AUTHORIZATION_CODE = "authorization_code"
    CLIENT_CREDENTIALS = "client_credentials"


@dataclass(frozen=True)
class TokenResponse:
    """OAuth 2.1 token response."""

    access_token: str
    token_type: str
    expires_in: int | None = None
    created_at: int | None = None
    scope: str | None = None
    id_token: str | None = None
    refresh_token: str | None = None


def fetch_token(
    endpoint: str,
    client_id: str,
    grant_type: GrantType,
    redirect_uri: str | None = None,
    code: str | None = None,
    pkce_secret: PKCESecret | None = None,
    client_secret: str | None = None,
) -> TokenResponse:
    """Fetch a token from the provider's token endpoint."""
    data = {
        "grant_type": format(grant_type),
        "client_id": client_id,
    }

    match grant_type:
        case GrantType.AUTHORIZATION_CODE:
            if not (pkce_secret and code and redirect_uri):
                raise TypeError(
                    "the authorization code flow is only allowed with PKCE "
                    "and requires both code and redirect URI."
                )
            data |= {
                "code": code,
                "redirect_uri": redirect_uri,
                "code_verifier": str(pkce_secret),
            }
        case GrantType.CLIENT_CREDENTIALS:
            if not client_secret:
                raise TypeError(
                    "the client credentials grant requires a client secret."
                )
            data |= {
                "client_secret": client_secret,
            }
        case _:
            raise ValueError("unsupported grant type.")

    request = Request(endpoint, data=urlencode(sorted(data.items())).encode())
    try:
        with urlopen(request) as response:
            token_data = json.load(response)
        return TokenResponse(
            **{
                key: value
                for key, value in token_data.items()
                # Ignore extra keys that are not token response fields
                if key in (field.name for field in fields(TokenResponse))
            }
        )
    except TypeError as error:
        print(json.dumps(token_data, indent=4))
        raise AuthorizationError(str(error))
    except HTTPError as error:
        print(json.dumps(json.load(error), indent=4))
        raise AuthorizationError(error.reason)
