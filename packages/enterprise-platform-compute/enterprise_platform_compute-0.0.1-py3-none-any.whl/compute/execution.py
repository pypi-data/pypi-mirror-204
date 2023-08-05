import gzip
import json
import os
from dataclasses import dataclass
from typing import Optional

import httpx
import polling2
from gql import gql
from gql.client import Client
from gql.transport.appsync_auth import AppSyncJWTAuthentication
from gql.transport.appsync_websockets import AppSyncWebsocketsTransport

from .client import ComputeGraphqlClient, PublicGraphqlClient

_PLATFORM_CORE_REALTIME_API_HOST = os.environ.get("PLATFORM_CORE_REALTIME_API_HOST")


def _build_async_transport(access_token: str):
    return AppSyncWebsocketsTransport(
        url=f"https://{_PLATFORM_CORE_REALTIME_API_HOST}/graphql",
        auth=AppSyncJWTAuthentication(
            host=_PLATFORM_CORE_REALTIME_API_HOST,
            jwt=access_token,
        ),
    )


POLL_QUERY = gql(
    """
        query ($id: ID!) {
            execution(executionId: $id) {
                id
                status
                outputObjectId
            } 
        }
    """
)

JOIN_SUBSCRIPTION = gql(
    """
        subscription($id: ID!) {
            subscribe(scope: $id) {
                scope
                data
            }
        }
    """
)

OUTPUT_DATA_OBJECT_QUERY = gql(
    """
        query ($id: ID!) {
            object(objectId: $id, asConcrete: false) {
                id
                getUrl
            }
        }
    """
)


@dataclass
class Execution:
    _api_key: str
    _compute_client: ComputeGraphqlClient
    _public_client: PublicGraphqlClient

    id: str
    package_object_id: str
    input_object_id: Optional[str] = None
    output_object_id: Optional[str] = None

    @classmethod
    def submit(cls, package: str, *, api_key: str):
        public_client = PublicGraphqlClient(token=api_key)
        compute_client = ComputeGraphqlClient(token=api_key)
        response = compute_client.execute(
            gql(
                """
                    mutation ($package: String!) {
                        submitGraphExecution(package: $package) {
                            id
                            packageObjectId
                        }
                    }
                """
            ),
            variable_values={"package": package},
        )
        return cls(
            _api_key=api_key,
            _public_client=public_client,
            _compute_client=compute_client,
            id=response["submitGraphExecution"]["id"],
            package_object_id=response["submitGraphExecution"]["packageObjectId"],
        )

    def _poll_for_completion(self):
        return self._compute_client.execute(POLL_QUERY, variable_values={"id": self.id})

    @staticmethod
    def _is_complete(response):
        return response["execution"]["status"] == "COMPLETED"

    def poll_for_completion(self):
        print("Running...")
        response = polling2.poll(
            self._poll_for_completion,
            check_success=self._is_complete,
            step=1,
            timeout=3600,
        )
        self.output_object_id = response["execution"]["outputObjectId"]
        print("Done.")

    async def join(self):
        async with Client(transport=_build_async_transport(self._api_key)) as client:
            async for message in client.subscribe(
                JOIN_SUBSCRIPTION,
                variable_values={"id": self.id},
            ):
                message_data_string = message["subscribe"]["data"]
                if message_data_string is not None:
                    message_data = json.loads(message_data_string)

    def get_results(self):
        response = self._public_client.execute(
            OUTPUT_DATA_OBJECT_QUERY,
            variable_values={"id": self.output_object_id},
        )

        print(response)

        return json.loads(
            gzip.decompress(httpx.get(response["object"]["getUrl"]).content).decode(
                "utf-8"
            )
        )
