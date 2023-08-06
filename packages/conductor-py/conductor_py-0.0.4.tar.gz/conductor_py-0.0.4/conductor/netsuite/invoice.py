from conductor import client
from conductor.graphql_client.input_types import SendIntegrationRequestInput
from conductor.graphql_client.send_integration_request import (
    SendIntegrationRequest,
)


def find_many(integration_connection_id: str) -> SendIntegrationRequest:
    return client.send_integration_request(
        input=SendIntegrationRequestInput(
            integrationConnectionId=integration_connection_id,
            requestObject={
                "invoice": {},
            },
        )
    )
