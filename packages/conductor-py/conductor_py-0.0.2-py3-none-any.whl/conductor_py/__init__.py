import toml
from conductor_py.graphql_client.client import Client


def _create_user_agent()-> str:
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)

    client_name: str = config["project"]["name"]
    client_version: str = config["project"]["version"]

    return f"{client_name}/{client_version} (Python)"

_server_url = "https://api.conductor.is"
client = Client(
    url=f"{_server_url}/graphql",
    headers={
        "User-Agent": _create_user_agent()
    },
)

def set_api_key(key: str):
    global client
    client.http_client.headers["Authorization"] = f"Bearer {key}"
    assert client.headers is not None
    client.headers["Authorization"] = f"Bearer {key}"


from conductor_py import netsuite
