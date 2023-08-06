"""
send requests to the Nextcloud API
"""
import requests
from requests_cache import CachedSession, enabled, disabled, install_cache

from .headers import NextcloudHeaders
from .i18n import _

install_cache('.ncb_requests', backend='sqlite')
session = CachedSession('.ncb_requests', backend='sqlite',
                        expire_after=90, use_temp=True)


class NextcloudRequests:
    """
    This class provides functionality to send requests to the Nextcloud API.

    :param base_url: The base URL of the Nextcloud instance.
    :param password: The password for the Nextcloud account.
    """

    def __init__(self, base_url, password):
        self.base_url = base_url
        self.password = password
        self.headers = NextcloudHeaders.create_headers(password)

    def send_request(self, endpoint, params=None, extra_headers=None):
        """
        Send a GET request to the specified Nextcloud API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :param params: Optional dictionary of query parameters to include in the request. Default is None.
        :param extra_headers: Optional dictionary of additional headers to include in the request. Default is None.
        :return: The JSON response from the server.
        :raises Exception: If the response status code is not 200.
        """
        session.get('https://httpbin.org/get')
        headers = self.headers.copy()
        if extra_headers:
            headers.update(extra_headers)

        url = f"{self.base_url}{endpoint}"
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10)

        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error: {url} {headers}, {params}. {e}") from None

        return response.json()

    def post_request(self, endpoint, json=None):
        """
        Send a POST request to the specified Nextcloud API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :param json: Optional dictionary containing the JSON payload to include in the request. Default is None.
        :return: The JSON response from the server.
        :raises Exception: If the response status code is not 200 or 201.
        """
        with disabled():
            headers = self.headers
            url = f"{self.base_url}{endpoint}"
            response = requests.post(
                url, headers=headers, json=json, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise Exception(
                    f"Error: {response.status_code}, {url} {headers}, {json}. {e}") from None

            return response.json()

    def delete_request(self, endpoint):
        """
        Send a DELETE request to the specified Nextcloud API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :return: None
        :raises Exception: If the response status code is not 204.
        """
        with disabled():
            headers = self.headers
            url = f"{self.base_url}{endpoint}"
            response = requests.delete(url, headers=headers, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error: {url} {headers}. {e}") from None
