from __future__ import annotations

import requests

from bigbucket.auth import authenticate
from bigbucket.utils import parse_response, handle_exception


class Client(object):
    def __init__(self, address: str = "http://localhost:8080",
                 timeout: float = 30.0, gcp_auth: bool = False):
        self.address = address
        self.timeout = timeout
        self.gcp_auth = gcp_auth
        self.headers = None
        self.jwt = None

    @authenticate
    def get_tables(self) -> list:
        try:
            r = requests.get(f"{self.address}/api/table",
                             timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        return parse_response(r)["tables"]

    def table(self, table_name: str) -> Table:
        return Table(table_name, address=self.address, timeout=self.timeout,
                     gcp_auth=self.gcp_auth, headers=self.headers, jwt=self.jwt)


class Table(object):
    def __init__(self, table_name: str, **kwargs):
        self.table_name = table_name
        self.address = kwargs.get("address")
        self.timeout = kwargs.get("timeout")
        self.gcp_auth = kwargs.get("gcp_auth")
        self.headers = kwargs.get("headers")
        self.jwt = kwargs.get("jwt")

    @authenticate
    def delete_table(self):
        try:
            params = {"table": self.table_name}
            r = requests.delete(f"{self.address}/api/table", params=params,
                                timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        parse_response(r)

    @authenticate
    def list_columns(self) -> list:
        try:
            params = {"table": self.table_name}
            r = requests.get(f"{self.address}/api/column", params=params,
                             timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        return parse_response(r)["columns"]

    @authenticate
    def delete_column(self, column_name: str):
        try:
            params = {"table": self.table_name, "column": column_name}
            r = requests.delete(f"{self.address}/api/column", params=params,
                                timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        parse_response(r)

    @authenticate
    def count_rows(self, prefix: str = None) -> int:
        try:
            params = {"table": self.table_name}
            if prefix:
                params["prefix"] = prefix
            r = requests.get(f"{self.address}/api/row/count", params=params,
                             timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        return int(parse_response(r)["rowsCount"])

    @authenticate
    def read_row(self, key: str, columns: list = None) -> dict:
        try:
            params = {"table": self.table_name, "key": key}
            if columns:
                params["columns"] = ",".join(columns)
            r = requests.get(f"{self.address}/api/row", params=params,
                             timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        return parse_response(r)[key]

    @authenticate
    def read_rows(self, prefix: str = None, columns: list = None, limit: int = None) -> dict:
        try:
            params = {"table": self.table_name}
            if prefix:
                params["prefix"] = prefix
            if columns:
                params["columns"] = ",".join(columns)
            if limit:
                params["limit"] = limit
            r = requests.get(f"{self.address}/api/row", params=params,
                             timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        return parse_response(r)

    @authenticate
    def set_row(self, key: str, column_value_map: dict):
        try:
            params = {"table": self.table_name, "key": key}
            r = requests.post(f"{self.address}/api/row", params=params, json=column_value_map,
                              timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        parse_response(r)

    @authenticate
    def delete_row(self, key: str):
        try:
            params = {"table": self.table_name, "key": key}
            r = requests.delete(f"{self.address}/api/row", params=params,
                                timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        parse_response(r)

    @authenticate
    def delete_rows(self, prefix: str):
        try:
            params = {"table": self.table_name, "prefix": prefix}
            r = requests.delete(f"{self.address}/api/row", params=params,
                                timeout=self.timeout, headers=self.headers)
        except Exception as e:
            handle_exception(e)

        parse_response(r)
