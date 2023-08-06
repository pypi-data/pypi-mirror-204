from ._util import hdc_service_client
from vhcs.util.query_util import with_query, PageRequest

_client = hdc_service_client("admin")


class template:
    @staticmethod
    def get(id: str, **kwargs):
        url = with_query(f"/v2/edge-deployments/{id}", **kwargs)
        return _client.get(url)

    @staticmethod
    def list(limit: int = 10, **kwargs):
        def _get_page(query_string):
            url = "/v2/templates?" + query_string
            return _client.get(url)

        return PageRequest(_get_page, limit, **kwargs).get()


class edge:
    @staticmethod
    def get(id: str, **kwargs):
        url = with_query(f"/v2/edge-deployments/{id}", **kwargs)
        return _client.get(url)

    @staticmethod
    def list():
        return _client.get("/v2/edge-deployments")


def test():
    print("test")
