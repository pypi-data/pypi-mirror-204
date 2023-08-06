# aioauthx

`aioauthx` adds [HTTPX](https://github.com/encode/httpx/blob/master/httpx/_auth.py)-style authentication strategies to [aiohttp](https://github.com/aio-libs/aiohttp) allowing `ClientSession`'s to support digest, negotiate, oauth2, etc.

## Installation

You can install `aioauthx` with `pip`

`pip install aioauthx`

See below for a list of optional dependencies

## Usage

`aioauthx` works by providing a framework to support different authentication schemes and wrapping that scheme in `ClientRequest` and `ClientResponse` types that can be passed directly to `ClientSession`. For example...

**Note: The `NegotiateAuth` flow requires `pywin32`. You can use the optional dependency.**

`pip install "aioauthx[win]"`

```python
from aioauthx import create_auth_handlers
from aioauthx.flows.negotiate import NegotiateAuth
from aiohttp import ClientSession


async def make_request(session: ClientSession) -> ...:
    resp = await session.get(...)
    ...
    
async def main() -> None:
    flow = NegotiateAuth(...)
    request_class, response_class = create_auth_handlers(flow)
    async with ClientSession(
        request_class=request_class, response_class=response_class
   	) as session:
        await make_request(session)
```

## Creating Flows

All flows inherit from `Auth`. The flow itself is an async generator that manipulates the request object being sent. To dispatch a request `yield`. Unlike HTTPX, you do not yield a request to the client, you manipulate a request in place. Yielding just lets the client know it can send the request as constructed. Upon executing the request, the client will `send()` the response back to the flow generator. We will illustrate this by building a basic auth flow (aiohttp supports basic auth out of the box, this is just for demonstration purposes)...

```python
from collections.abc import AsyncGenerator

from aioauthx import Auth
from aiohttp import ClientRequest, ClientResponse, hdrs
from aiohttp.connector import Connection


class BasicAuth(Auth):
    def __init__(self, username: str, password: str) -> None:
        self.username, self.password = username, password
        
    async def flow(
        self,
        request: ClientRequest,
        connection: Connection
   	) -> AsyncGenerator[None, ClientResponse]:
        userpass = b":".join((to_bytes(self.username), to_bytes(self.password)))
        token = b64encode(userpass).decode()
        auth_header = f"Basic {token}"
        request.headers[hdrs.AUTHORIZATION] = auth_header
        
        # In terms of the auth scheme we are done so we could just yield here
        # and that would be it. Like so...
        # yield
        # return
        
        # However, if we want to see how to use the response we can yield and
        # expect the response...
        response = yield
        print(response.status)
        
```

## Optional Dependencies

- aioauthx[win] -> pywin32