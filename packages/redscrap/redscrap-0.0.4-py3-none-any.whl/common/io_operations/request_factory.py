import httpx
from typing import Dict, Any, Optional, List


class RequestFactory:
    """A class that provides a simple interface for making HTTP requests using the httpx module."""

    def __init__(self, timeout: Optional[float] = None, headers: Optional[Dict[str, str]] = None) -> None:
        """
        Initializes a new instance of the RequestFactory class.

        Args:
            timeout (float, optional): The maximum time to wait for a response, in seconds. Defaults to None.
            headers (Dict[str, str], optional): A dictionary of additional headers to include with each request. \
            Defaults to None.
        """
        self.timeout: Optional[float] = timeout
        self.headers: Dict[str, str] = headers or {}

    def _get_client(self) -> httpx.Client:
        """
        Returns a new instance of the httpx Client class, configured with the factory's timeout and headers.

        Returns:
            httpx.Client: A new httpx client instance.
        """
        transport = httpx.HTTPTransport(retries=3)
        return httpx.Client(transport=transport, headers=self.headers, timeout=self.timeout)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) \
            -> httpx.Response:
        """
        Sends an HTTP GET request to the specified path, with the specified query parameters and headers.

        Args:
            path (str): The path to send the request to.
            params (Dict[str, Any], optional): A dictionary of query parameters to include with the request. \
            Defaults to None.
            headers (Dict[str, str], optional): A dictionary of additional headers to include with the request. \
            Defaults to None.

        Returns:
            httpx.Response: The response from the server.

        Raises:
            httpx.RequestError: If an error occurs while sending the request.
        """
        client = self._get_client()
        try:
            response = client.get(path, params=params, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            raise exc
        finally:
            client.close()

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) \
            -> httpx.Response:
        """
        Sends an HTTP POST request to the specified path, with the specified request data and headers.

        Args:
            path (str): The path to send the request to.
            data (Dict[str, Any], optional): A dictionary of data to include with the request. Defaults to None.
            headers (Dict[str, str], optional): A dictionary of additional headers to include with the request. \
            Defaults to None.

        Returns:
            httpx.Response: The response from the server.

        Raises:
            httpx.RequestError: If an error occurs while sending the request.
        """
        client = self._get_client()
        try:
            response = client.post(path, json=data, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            raise exc
        finally:
            client.close()

    def put(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) \
            -> httpx.Response:
        """
        Sends an HTTP PUT request to the specified path, with the specified request data and headers.

        Args:
            path (str): The path to send the request to.
            data (Dict[str, Any], optional): A dictionary of data to include with the request. Defaults to None.
            headers (Dict[str, str], optional): A dictionary of additional headers to include with the request.\
            Defaults to None.

        Returns:
            httpx.Response: The response from the server.

        Raises:
            httpx.RequestError: If an error occurs while sending the request.
        """
        client = self._get_client()
        try:
            response = client.put(path, json=data, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            raise exc
        finally:
            client.close()

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Sends a DELETE request to the specified path using the client created by the factory.

        Args:
            path (str): The path to send the request to.
            headers (Optional[Dict[str, str]]): A dictionary of headers to include in the request.

        Returns:
            httpx.Response: The response object returned by the request.

        Raises:
            httpx.RequestError: If an error occurs during the request.
        """

        client = self._get_client()
        try:
            response = client.delete(path, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            raise exc
        finally:
            client.close()

    def patch(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) \
            -> httpx.Response:
        """
        Sends a PATCH request to the specified path using the client created by the factory.

        Args:
            path (str): The path to send the request to.
            data (Optional[Dict[str, Any]]): A dictionary of data to include in the request.
            headers (Optional[Dict[str, str]]): A dictionary of headers to include in the request.

        Returns:
            httpx.Response: The response object returned by the request.

        Raises:
            httpx.RequestError: If an error occurs during the request.
        """
        client = self._get_client()
        try:
            response = client.patch(path, json=data, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            raise exc
        finally:
            client.close()

    def get_access_token(self, client_id, secret_token, username, password, main_constants) -> Dict[str, str]:
        """
        Sends a POST request to the Reddit API to request an access token using the provided credentials.

        Args:
            client_id (str): The client ID for the Reddit API.
            secret_token (str): The secret token for the Reddit API.
            username (str): The Reddit username to authenticate with.
            password (str): The password for the Reddit account to authenticate with.
            main_constants (class): An object containing constants related to the Reddit API.

        Returns:
            Dict[str, str]: A dictionary containing the access token and other relevant information.

        Raises:
            httpx.RequestError: If an error occurs during the request.
        """
        auth = httpx.BasicAuth(client_id, secret_token)
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        headers = main_constants.reddit_headers

        response = httpx.post(
            "{}/api/v1/access_token".format(main_constants.reddit_url),
            auth=auth,
            data=data,
            headers=headers
        )

        response.raise_for_status()  # raise an exception if there is an error with the request

        return response.json()
