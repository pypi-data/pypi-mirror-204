from graphql_client.client import Client

server_url = "https://api.conductor.is"
api_key = None
client = Client(
    url=f"{server_url}/graphql",
    headers={
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "conductor-py/0.0.0",
    },
)

from conductor_py import netsuite
