import time
import json
from typing import Any
from ._util import hdc_service_client
from vhcs.util.query_util import with_query, PageRequest

_client = hdc_service_client("lcm")


class template:
    @staticmethod
    def get(id: str, **kwargs: Any):
        url = with_query(f"/v1/templates/{id}", **kwargs)
        return _client.get(url)

    @staticmethod
    def list(limit: int = 20, name: str = None, **kwargs):
        def _get_page(query_string):
            url = "/v1/templates?" + query_string
            return _client.get(url)

        ret = PageRequest(_get_page, limit, **kwargs).get()
        if name:
            # filter_fn = lambda t : t.name.find(name) >= 0
            def filter_fn(t):
                return t.name.find(name) >= 0

            ret = list(filter(filter_fn, ret))
        return ret

    @staticmethod
    def delete(id: str, org_id: str, force: bool):
        resp = _client.delete(f"/v1/templates/{id}?org_id={org_id}&force={force}")
        return _convert_resp(resp)

    @staticmethod
    def create(template: dict):
        url = "/v1/templates"
        url += "/" + template["providerType"].lower()
        return _client.post(url=url, json=template)

    @staticmethod
    def wait(
        id: str,
        expected_status: list,
        timeout_seconds: int,
        exclude_status: list = ["ERROR"],
        interval_seconds: int = 10,
    ):
        start = int(time.time())
        while True:
            t = template.get(id)
            if not t:
                msg = f"Error waiting for template {id}. Not found."
                raise Exception(msg)

            status = t.status

            if status in expected_status:
                return t

            if status in exclude_status:
                msg = f"Error waiting for template {id}. Current status is {status}, which is not expected."
                raise Exception(msg)

            now = int(time.time())
            elapsed = now - start

            if elapsed > timeout_seconds:
                msg = f"Timeout waiting for template {id}. Current: {status}, expect: {expected_status}"
                raise Exception(msg)

            delay = min(interval_seconds, timeout_seconds - elapsed)
            time.sleep(delay)

            print(f"Waiting for template {id}. Expected={exclude_status}, current={status}...")


class provider:
    @staticmethod
    def get(id: str, **kwargs: Any):
        url = with_query(f"/v1/providers/{id}", **kwargs)
        return _client.get(url)

    @staticmethod
    def list(limit: int = 20, **kwargs):
        def _get_page(query_string):
            url = "/v1/providers?" + query_string
            return _client.get(url)

        return PageRequest(_get_page, limit, **kwargs).get()

    @staticmethod
    def delete(id: str):
        resp = _client.delete(f"/v1/providers/{id}")
        return _convert_resp(resp)

    @staticmethod
    def create(data: dict):
        url = "/v1/providers/" + data["type"].lower()
        return _client.post(url, json=data)


def _convert_resp(resp):
    if resp:
        resp.read()
        try:
            json.loads(resp.text)
        except:
            return resp.text


def test():
    print("test")
