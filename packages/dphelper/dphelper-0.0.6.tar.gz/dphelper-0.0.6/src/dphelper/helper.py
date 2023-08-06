from pprint import pprint as _pprint
import typing as _typing
import urllib.parse as _parse

import requests as _requests

from .connection import FetchModule as __FetchModule
from .snapshot import SnapshotModule as _SnapshotModule


class DPHelper(__FetchModule):  # also includes Config
    def __init__(
        self,
        *,
        is_verbose=False,
        request_drop_on_failure_count=4,
        request_initial_sleep_after_failure_in_s=3,
        request_sleep_increase_power=2,
        backend_url="https://data-platform-backend-4ddpl.ondigitalocean.app",
    ) -> None:
        self._init_config_values()
        self.IS_VERBOSE = bool(is_verbose)
        self.REQUEST_DROP_ON_FAILURE_COUNT = int(request_drop_on_failure_count)
        self.REQUEST_INITIAL_SLEEP_AFTER_FAILURE_IN_S = int(
            request_initial_sleep_after_failure_in_s
        )
        self.REQUEST_SLEEP_INCREASE_POWER = int(request_sleep_increase_power)
        self.set_backend_url(str(backend_url))
        self.snapshot = _SnapshotModule(config=self, fetcher=self)

    def __get_utils_url(self, path: str) -> str:
        "joins root url with specified path"
        # appending "/" to root so path gets joined, not overwriten
        # >>> "http://q.w/r" == _parse.urljoin("http://q.w/e", "r")
        # >>> "http://q.w/e/r" == _parse.urljoin("http://q.w/e" + "///////", "r")
        url = _parse.urljoin(self.BACKEND_URL + "/", self.BACKEND_UTILS_PATH)
        return _parse.urljoin(url + "/", path)

    def parse_rows(
        self, schema: list[str], data: list[list[str]], verbose: None | bool = None
    ) -> list[_typing.Any]:
        """parses from (look below) to list of dict (look even more below)
        >>> schema = [header1, header2, ...]
        >>> data = [
            [cell1_value, cell2_value, ...],  # 1st row
            [Cell1_value, Cell2_value, ...],  # 2nd row
            ...
        ]

        returns list of dict:
        >>> return_value = [
            {header1: cell1_value, header2: cell2_value}, # 1st row
            {header2: Cell1_value, header2: Cell2_value}, # 2nd row
            ...
        ]

        :param schema: list of headers (eg price, area, floor, id, balcony, status, ...)
        :param data: two-dimensional list of data; It will be parsed as `data[row][column]`
        :param verbose: shall error text be printed?"""
        # local verbose > config verbose
        verbose = self.IS_VERBOSE if verbose is None else verbose

        data = {
            "schema": schema,
            "data": data,
        }

        response = self._request_or_repeat(
            _requests.post,
            url=self.__get_utils_url("parse"),
            json=data,
            params={"cell_cnt": len(schema) * len(data)},
        )

        try:
            json_data: dict = response.json()
            is_success = json_data["is_success"]
            if not is_success and verbose:
                _pprint(json_data.get("error"))
            return json_data.get("results", [])
        except Exception:
            raise RuntimeError(
                "Could not understand remote server response for rows-parsing. "
                f"Try updating {self.PACKAGE_NAME} and try again"
            )

    @staticmethod
    def update_table(
        data: list[dict],
        f_check: _typing.Callable[[dict], bool],
        f_update: _typing.Callable[[dict], dict],
    ) -> list[dict]:
        """updates matching table rows using provided `f_update`. Returns altered table.

        :param data: list of dictionaries - list of rows.
        :param f_check: function that will return `True` if the row has to be altered.
        This function will be checked upon each row.
        :param f_update: function whose returned value will be applied to checked rows.
        :return: Altered version of original table
        """
        results: list[dict] = []
        for row in data:
            result = {}
            result.update(row)
            if f_check(row):
                payload = f_update(row)
                result.update(payload)

            results.append(result)

        return results
