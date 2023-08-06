"""Command-line interface for the OpenID Connect client."""
import argparse
import json
import sys
import traceback
from dataclasses import asdict
from pathlib import Path
from urllib.error import URLError

from .config import (
    DEFAULT_CONFIG_FILE,
    DEFAULT_OIDC_SCOPE,
    DEFAULT_REDIRECT_URI,
    ClientProfile,
    ProviderConfig,
    read_profile,
)
from .discovery import fetch_provider_config
from .error import AuthorizationError, ProviderConfigError, TokenRequestParamError
from .lib import login


def _get_provider_meta(
    args: argparse.Namespace,
) -> tuple[ProviderConfig, ClientProfile]:
    """Get OIDC provider metadata from CLI args."""
    profile = read_profile(
        Path(args.config_file), profile_name=args.profile, overrides=args
    )
    try:
        provider_config = fetch_provider_config(profile.issuer)
        if args.subcommand == "get-provider-metadata":
            print(json.dumps(asdict(provider_config), indent=4))
    except URLError as error:
        if args.debug:
            traceback.print_exception(error)
        exit(f"Failed to query provider configuration: {error.reason}")

    return provider_config, profile


def _login(args: argparse.Namespace) -> None:
    """Perform OIDC login from CLI args."""
    provider_config, profile = _get_provider_meta(args)

    try:
        auth = login(
            provider_config,
            client_id=profile.client_id,
            client_secret=profile.client_secret,
            redirect_uri=profile.redirect_uri,
            scope=profile.scope,
            interactive=args.interactive,
        )
    except (ProviderConfigError, TokenRequestParamError) as error:
        if args.debug:
            traceback.print_exception(error)
        exit(f"Login configuration error: {error}")
    except AuthorizationError as error:
        if args.debug:
            traceback.print_exception(error)
        exit(f"Login failed: {error}")
    except KeyboardInterrupt:
        exit("Login cancelled.")

    if args.only_id_token:
        print(auth.id_token)
    elif args.only_access_token:
        print(auth.access_token)
    else:
        print(json.dumps(asdict(auth), indent=4))


def main() -> None:
    """Entrypoint to the OIDC client command-line interface."""
    # Main parser
    parser = argparse.ArgumentParser()

    # Common arguments
    parser.add_argument(
        "--debug", "-d", help="provide debug traces", action="store_true", default=False
    )
    parser.add_argument(
        "--config-file",
        help="config file path, defaults to 'pyproject.toml'",
        default=DEFAULT_CONFIG_FILE,
    )
    parser.add_argument("--profile", help="profile key in the config file section")

    # Subparsers
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid OIDC client subcommands",
        dest="subcommand",
        required=True,
    )

    # Login subcommand parser
    parser_login = subparsers.add_parser("login")
    parser_login.add_argument(
        "--interactive",
        "-i",
        help="open a web browser to authenticate with the provider",
        action="store_true",
    )
    overrides = parser_login.add_argument_group(
        title="🌐🔧 OpenID Connect client settings",
        description="↳ override config file active profile and environment variables",
    )
    overrides.add_argument("--issuer", help="issuer URL")
    overrides.add_argument("--client-id", help="client ID")
    overrides.add_argument(
        "--client-secret-stdin",
        help="take the client secret from stdin",
        action="store_true",
    )
    overrides.add_argument(
        "--redirect-uri",
        help=f"authorization code redirect URI (default: '{DEFAULT_REDIRECT_URI}')",
    )
    overrides.add_argument(
        "--scope",
        help=f"scope (can be given multiple times, default: '{DEFAULT_OIDC_SCOPE}')",
        default=[],
        action="append",
    )
    outputs = parser_login.add_mutually_exclusive_group()
    outputs.add_argument(
        "--only-id-token", help="only output the ID token", action="store_true"
    )
    outputs.add_argument(
        "--only-access-token", help="only output the access token", action="store_true"
    )
    parser_login.add_argument(
        "stdin",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help=argparse.SUPPRESS,
    )
    parser_login.set_defaults(func=_login)

    # Get Provider Metadata subcommand parser
    parser_get_provider_meta = subparsers.add_parser("get-provider-metadata")
    parser_get_provider_meta.add_argument("issuer", help="🌐 OIDC issuer URL", nargs="?")
    parser_get_provider_meta.set_defaults(func=_get_provider_meta)

    # Finally, parse
    args = parser.parse_args()
    args.func(args)
