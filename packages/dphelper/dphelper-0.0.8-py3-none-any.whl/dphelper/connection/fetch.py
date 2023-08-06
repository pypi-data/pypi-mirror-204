import typing as _typing
import logging as _logging

import requests as _requests
from requests import Response as _Response
from requests.exceptions import ConnectionError as _ConnectionError
from time import sleep as _sleep
from urllib import parse as _parse
from fake_headers import Headers as _Headers

from ..config import Config as __Config


class FetchModule(__Config):
    def create_headers(
        self, authority: str | None = None, extra_headers: dict = {}
    ) -> dict:
        """create prefilled headers with custom authority value, append extra_headers.
        :param authority: what authority to use? If None, then no authority will be set.
        :param extra_headers: dict of headers that shall be appended
        :return: ready to use headers
        """
        headers = {}
        if authority is not None:
            headers["authority"] = authority
        headers.update(self.DEFAULT_HEADERS)
        headers.update(extra_headers)
        return headers

    def _get_headers_or_generate(self, headers: None | dict = None) -> dict:
        "return headers or generate new ones"
        if isinstance(headers, dict):
            return headers
        new_headers = _Headers().generate()
        # generates:
        # 'Accept': '*/*'
        # 'Connection': 'keep-alive'
        # 'User-Agent': random_agent
        new_headers.update(self.HEADERS_UPDATE_ON_EMPTY)
        return new_headers

    @staticmethod
    def _compare_headers(left_headers: dict, right_headers: dict) -> str:
        """returns headers differences for debug purposes"""
        normalize = (  # keys to lowercase
            lambda headers: None
            if headers is None
            else {str(key).lower(): value for key, value in headers.items()}
        )
        left_headers = normalize(left_headers)
        right_headers = normalize(right_headers)
        if left_headers == right_headers:
            return "Headers equal"
        elif left_headers is None:
            return "Left-header is None"
        elif right_headers is None:
            return "Right-header is None"

        # what is unique in left-headers? in right-headers? what is unequal?
        exclusives = []
        unequalities = []
        left_keys, right_keys = set(left_headers), set(right_headers)
        exclusives.extend(
            f"exclusive to left-headers: {key}" for key in left_keys - right_keys
        )
        exclusives.extend(
            f"exclusive to right-headers: {key}" for key in right_keys - left_keys
        )

        for key in left_keys.intersection(right_keys):  # shared keys
            if left_headers[key] != right_headers[key]:
                unequalities.append(f"left-headers != right-headers at ({key}):")
                unequalities.append(f"({left_headers[key]}) != ({right_headers[key]})")

        return "\n".join(unequalities + exclusives)

    def __get_proxy_full_url(self):
        url = _parse.urljoin(self.BACKEND_URL, self.BACKEND_UTILS_PATH)
        return _parse.urljoin(url, "proxy/")

    def _request_or_repeat(self, function: callable, *args, **kwargs) -> _Response:
        """Makes a request (call provided function with args and kwargs).
        * If it fails because of ConnectionError, retries;
        * If it fails because status_code >= 500, retries;
        retry count and sleep times are specified in package_consts.py

        :param function: function to call; expected to get response object from it.
        :param *args: what args to pass to function.
        :param **kwargs: what kwargs to pass to function.
        :return: `Response` or raises RuntimeError after all failures
        """

        failures_count = 0
        sleep_time = self.REQUEST_INITIAL_SLEEP_AFTER_FAILURE_IN_S
        failure_reason = ""

        def _handle_failure():
            nonlocal failures_count, sleep_time
            sleep_time = (
                sleep_time**self.REQUEST_SLEEP_INCREASE_POWER
                if failures_count > 0
                else sleep_time
            )
            failures_count = failures_count + 1

        while failures_count < self.REQUEST_DROP_ON_FAILURE_COUNT:
            if failures_count > 0:
                if self.IS_VERBOSE:
                    _logging.error(
                        f"Request failed: {failure_reason}. Retrying in {sleep_time} seconds"
                    )
                _sleep(sleep_time)
            try:
                response: _Response = function(*args, **kwargs)
                if response.status_code >= 500:
                    # server tripped, not we (internal server error)
                    raise RuntimeError
                else:
                    return response
            except _ConnectionError:
                _handle_failure()
                failure_reason = "Server inexistant or check Network settings"
            except RuntimeError:
                _handle_failure()
                failure_reason = "Remote server had an internal error"

        raise RuntimeError(
            f"[internal] Could not make connection for {self.REQUEST_DROP_ON_FAILURE_COUNT} times. Last reason of failure: {failure_reason}"
        )

    @staticmethod
    def _response_ok_or_raise(response: _requests.Response) -> None:
        """Raises ValueError if response returned failure code"""
        try:
            response.raise_for_status()
        except Exception as ex:
            raise ValueError(
                "The response was not ok. "
                f"Response code: {response.status_code} "
                f"response text: {response.text}"
            ) from ex

    def fetch_html(
        self,
        url: str,
        *,
        proxy_provider: None | _typing.Literal["scrapingbee"] = None,
        params: None | dict = None,
        headers: None | dict = None,
        data: None | _typing.Any = None,
        json: None | _typing.Any = None,
        cookies: None | dict = None,
        method: _typing.Literal["POST", "GET", "PUT", "PATCH", "DELETE"] = "GET",
        is_repeat_on_failure: bool = True,
        proxy_params: None | dict = None,
        stream: None | bool = None,
    ) -> _requests.Response:
        headers = self._get_headers_or_generate(headers)
        # prepare perform_method and call it with request_kwargs
        if proxy_provider is None:
            # no proxy
            perform_method = (
                _requests.request  # request once
                if not is_repeat_on_failure
                else lambda *args, **kwargs: self._request_or_repeat(
                    _requests.request, *args, **kwargs
                )  # request and retry on 5xx, connection errors
            )

            request_kwargs = {
                "method": method,
                "url": url,
                "params": params,
                "headers": headers,
                "cookies": cookies,
                "data": data,
                "json": json,
                "stream": stream,
            }
        else:
            # proxy yes
            # whoops cookies
            if cookies is not None:
                raise NotImplementedError(
                    "Current ",
                    self.PACKAGE_NAME,
                    " version does not support cookies in Proxy.",
                )
            # perform_method + request_kwargs
            perform_method = (
                _requests.post  # once
                if not is_repeat_on_failure
                else lambda *args, **kwargs: self._request_or_repeat(
                    _requests.post,
                    *args,
                    **kwargs,
                )
            )

            request_kwargs = {
                "url": self.__get_proxy_full_url(),
                "params": {"provider": str(proxy_provider)},
                "json": {
                    "url": url,
                    "headers": headers,
                    "params": params,
                    "data": data,
                    "json": json,
                    "method": method,
                    "proxy_params": proxy_params,
                },
                "stream": stream,
            }

        # do request
        return perform_method(**request_kwargs)

    def from_url(self, url, verify=True, headers: None | dict = None):
        "return content with stripped trailing whitespaces (newlines) from each line"
        headers = self._get_headers_or_generate(headers)
        response = _requests.get(url, verify=verify, headers=headers)
        return "".join([line.decode("utf-8").strip() for line in response.iter_lines()])
