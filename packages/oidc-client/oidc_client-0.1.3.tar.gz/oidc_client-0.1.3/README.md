OIDC Client
===========

A pure-Python OpenID Connect client supporting OAuth 2.1 authorization flows, built for Python 3.10+ with minimal dependencies.

OAuth 2.1 authorization flows include:
- the **authorization code** flow, for interactive user login;
- the **client credentials** flow, for confidential machine-to-machine communication.

This OIDC Client supports reading configuration profiles from a `pyproject.toml` file.


Requirements
------------

Python 3.10+



Installation
------------

```console
pip install oidc-client
```


Configuration
-------------

To enable interactive login for your project, add the following to your `pyproject.toml`:
```toml
[tool.oidc]
issuer = "https://example.com"  # URL of your OIDC provider
client_id = "<application ID>"  # Application ID given by your OIDC provider
```


Examples
--------

```console
# To log-in as a user, using a web browser:
oidc login --interactive
```


License
-------

This project is licensed under the terms of the MIT license.


A [YZR](https://www.yzr.ai/) Free and Open Source project.
