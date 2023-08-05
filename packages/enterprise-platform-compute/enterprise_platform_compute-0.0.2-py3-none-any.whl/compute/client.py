from gql import Client
from gql.transport.requests import RequestsHTTPTransport

_PLATFORM_CORE_PUBLIC_GRAPHQL_HOST = (
    "https://public.enterprise-platform-development.com/graphql"
)
_PLATFORM_COMPUTE_PUBLIC_GRAPHQL_HOST = (
    "https://compute.enterprise-platform-development.com/graphql"
)


class ClientBase(Client):
    url: str

    def __init__(self, *, token: str, **kwargs):
        headers = {"authorization": f"mchugh::token::{token}"}
        transport = RequestsHTTPTransport(self.url, headers=headers, timeout=120)
        super().__init__(transport=transport, **kwargs)


class ComputeGraphqlClient(ClientBase):
    url = _PLATFORM_COMPUTE_PUBLIC_GRAPHQL_HOST


class PublicGraphqlClient(ClientBase):
    url = _PLATFORM_CORE_PUBLIC_GRAPHQL_HOST
