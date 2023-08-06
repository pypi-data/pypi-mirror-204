from typing import Optional

import pytest
from graphql_api.mapper import GraphQLMetaKey

from requests import request, ConnectTimeout, ReadTimeout
from graphql_http_server import GraphQLHTTPServer


def is_graphql_api_installed():
    try:
        import graphql_api
        assert graphql_api
    except ImportError:
        return False

    return True


def available(url, method="GET"):
    try:
        response = request(
            method,
            url,
            headers={"Accept": "text/html"},
            timeout=5,
            verify=False
        )
    except (ConnectionError, ConnectTimeout, ReadTimeout):
        return False

    if response.status_code == 400 or response.status_code == 200:
        return True

    return False


@pytest.mark.skipif(
    not is_graphql_api_installed(),
    reason="GraphQL-API is not installed"
)
class TestGraphQLAPI:

    def test_graphql_api(self):
        from graphql_api import GraphQLAPI

        api = GraphQLAPI()

        @api.type(root=True)
        class RootQueryType:

            @api.field
            def hello(self, name: str) -> str:
                return f"hey {name}"

        server = GraphQLHTTPServer.from_api(api=api)

        response = server.client().get('/?query={hello(name:"rob")}')

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"hey rob"}}'

    def test_graphql_api_error(self):
        from graphql_api import GraphQLAPI

        api = GraphQLAPI()

        @api.type(root=True)
        class RootQueryType:

            @api.field
            def hello(self, error: bool = True) -> str:
                if error:
                    raise Exception("hello error")
                return ""

            @api.field
            def optional_hello(self, error: bool = True) -> Optional[str]:
                if error:
                    raise Exception("optional hello error")
                return ""

            @api.field({GraphQLMetaKey.error_protection: False})
            def raise_hello(self) -> str:
                raise Exception("optional hello error")

        server = GraphQLHTTPServer.from_api(api=api)

        response = server.client().get('/?query={hello}')

        assert response.status_code == 200
        assert response.json
        assert "data" not in response.json
        assert "errors" in response.json

        response = server.client().get(
            '/?query={hello(error: false) optionalHello}'
        )

        assert response.status_code == 200
        assert response.json
        assert "data" in response.json
        assert "errors" in response.json

        with pytest.raises(Exception):
            server.client().get(
                '/?query={raiseHello}'
            )

