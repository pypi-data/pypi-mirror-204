from conductor_py import client
from graphql_client.input_types import SendIntegrationRequestInput


def find_many(integration_connection_id: str) -> list:
    return client.send_integration_request(
        input=SendIntegrationRequestInput(
            integration_connection_id=integration_connection_id,
            requestObject={
                "invoice": {},
            },
        )
    )
