"""TLS utilities."""
import ssl
from importlib.resources import as_file, files
from socket import socket


def setup_tls(socket: socket) -> socket:
    """Wrap a socket with a default TLS (formerly SSL) context."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    with (
        as_file(files(__package__).joinpath("localhost.crt")) as certfile,
        as_file(files(__package__).joinpath("localhost.key")) as keyfile,
    ):
        context.load_cert_chain(certfile, keyfile)
    return context.wrap_socket(socket, server_side=True)
