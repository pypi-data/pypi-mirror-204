from typing import Optional, Dict, Union
from loguru import logger       # type: ignore

from common.exceptions.main_exceptions import UserNotFoundException, TokenErrorException  # type: ignore
from common.logging.logging_setup import LoggingSetup   # type: ignore
from common.constants.common_constants import CommonConstants     # type: ignore
from common.io_operations.request_factory import RequestFactory     # type: ignore


class RedditApi:
    """
        A class that provides functions to access Reddit API.

    Methods:
        def generate_headers(self, token: str) -> Dict[str, str]:
            Generates headers for a Reddit API request.

        def generate_reddit_api_token(self, verbose: bool = False) -> str:
             Generate a Reddit API token using the user's credentials.

        def get_logged_user_profile(self, verbose: bool) -> Union[Dict, None]:
            Retrieve the logged-in user's profile information.

        def generate_params_for_reddit_api_req(self, after: Optional[str], before: Optional[str], count: Optional[int],
            limit: Optional[int], show: Optional[str], sr_detail: bool) -> Dict[str, str]:
            Generate a dictionary of parameters to be used in a Reddit API request.
    """
    def __init__(self, client_id, secret_token, username, password):
        self.logging_setup = LoggingSetup()
        self.main_constants = CommonConstants()
        self.request_factory = RequestFactory()
        self.client_id = client_id
        self.secret_token = secret_token
        self.username = username
        self.password = password

    def generate_headers(self, token: str) -> Dict[str, str]:
        """
        Generates headers for a Reddit API request.

        Args:
            token (str): A Reddit API access token.

        Returns:
            Dict[str, str]: A dictionary of headers with authorization token added.
        """
        headers: dict[str, str] = {**self.main_constants.reddit_headers, **{"Authorization": "bearer {}".format(token)}}
        return headers

    def generate_reddit_api_token(self) -> str:
        """Generate a Reddit API token using the user's credentials.

        Raises:
            TokenErrorException: If the request to obtain the token fails.

        Returns:
            str: The generated Reddit API token.
        """

        response = self.request_factory.get_access_token(self.client_id, self.secret_token, self.username,
                                                         self.password, self.main_constants)
        token = response["access_token"]
        msg = "Generated Reddit API token: {}".format(token)
        logger.info(msg)
        return token

    def get_logged_user_profile(self) -> Union[Dict, None]:
        """
        Retrieve the logged-in user's profile information.

        Returns:
            Union[Dict, None]: Returns a dictionary of the user profile information if successful,
            otherwise returns None.

        Raises:
            UserNotFoundException: If the user profile is unavailable or could not be reached.
        """
        # Generating the URL leading to the desired subreddit
        url = "{}/api/v1/me".format(self.main_constants.reddit_api_base_url)
        token = self.generate_reddit_api_token()
        headers = {**self.main_constants.reddit_headers, **{"Authorization": "bearer {}".format(token)}}

        response = None

        try:
            res = self.request_factory.get(url, headers=headers)

            if res:
                response = res.json()

        except UserNotFoundException as exc:
            msg = "Your user profile is unavailable or couldn't be reached at this moment"
            logger.exception(msg)
            raise UserNotFoundException(msg) from exc

        return response

    def generate_params_for_reddit_api_req( self, after: Optional[str], before: Optional[str], count: Optional[int],
                                            limit: Optional[int], show: Optional[str], sr_detail: Optional[bool]) \
            -> Dict[str, object]:
        """
        Generate a dictionary of parameters to be used in a Reddit API request.

        Args:
            after (Optional[str]): The fullname of the post to start after.
            before (Optional[str]): The fullname of the post to start before.
            count (Optional[int]): The number of items in the listing to skip.
            limit (Optional[int]): The maximum number of items to return.
            show (Optional[str]): The types of items to show.
            sr_detail (Optional[bool]): Whether to return details about the subreddit.

        Returns:
            A dictionary containing the specified parameters for a Reddit API request.
        """
        params = {
            "after": after if after is not None else "",
            "before": before if before is not None else "",
            "count": count if count is not None else "",
            "limit": limit if limit is not None else "",
            "show": show if show is not None else "",
            "sr_detail": sr_detail if sr_detail is not None else "",
        }

        return params
