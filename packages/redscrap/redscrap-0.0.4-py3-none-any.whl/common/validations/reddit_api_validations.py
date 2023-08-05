from typing import Optional, List
from loguru import logger       # type: ignore
import json

from common.exceptions.main_exceptions import SubredditNotFoundException, UserNotFoundException, TokenErrorException  # type: ignore
from common.logging.logging_setup import LoggingSetup   # type: ignore
from common.constants.common_constants import CommonConstants       # type: ignore
from common.io_operations.request_factory import RequestFactory       # type: ignore
from core.api.reddit_api import RedditApi       # type: ignore


class RedditApiValidations:
    """
    A class that provides a number of methods to expose the reddit API

    Methods:
        - def validate_subreddits_list(self, subreddits): Validates a list of subreddits

        - def validate_subreddit(self, subreddit): Validates if a subreddit exists

        - def check_if_subreddit_exists(self, token: str, subreddit: str) -> Optional[bool]:
            Checks if the given subreddits exists on Reddit API.

        - def validate_reddit_user(self, reddit_user: str, verbose: bool) -> Optional[bool]:
            Checks if the given username exists on Reddit API.

        - def validate_user(self, token: str, reddit_user: str) -> Optional[bool]:
            Checks if the given username exists on Reddit API.

        - def validate_user_v2(self, reddit_user: str) -> Optional[bool]:
            Checks if the given username exists on Reddit API.
    """

    def __init__(self):
        self.logging_setup = LoggingSetup()
        self.main_constants = CommonConstants()
        self.request_factory = RequestFactory()
        self.reddit_api = RedditApi(self.main_constants.client_id, self.main_constants.secret_token,
                                    self.main_constants.username, self.main_constants.password)

    def validate_subreddits_list(self, subreddits: List[str], verbose: bool):
        """
        Validates a list of subreddits

        Args:
            subreddits (str): list of comma or semicolon separated values
            verbose (bool): Controls the verbosity level
        """
        logger.debug("[4] VALIDATE SUBREDDITS STEP")

        for sub_red in subreddits:
            if self.validate_subreddit(sub_red, verbose) is False:
                message = "The provided subreddit {} was not found. Please provide a valid one".format(sub_red)
                raise SubredditNotFoundException(message)

        logger.info(
            "Validation step: {}".format(self.main_constants.check_mark_symbol)) if verbose else None

    def validate_subreddit(self, subreddit: str, verbose: bool) -> Optional[bool]:
        """
        Checks if the given subreddit exists on Reddit API.

        Args:
            subreddit (str): The name of the subreddit to check.
            verbose: (bool): Controls the verbosity level

        Returns:
            bool: True if the subreddit exists, False otherwise.

        Notes:
            According to Reddit's API rules changed the client's User-Agent string to something unique and descriptive,
            including the target platform, a unique application identifier, a version string, and your username
            as contact information, in the following format
        """

        # add authorization to our headers dictionary
        url = "{}/r/{}/about".format(self.main_constants.reddit_api_base_url, subreddit)
        token = self.reddit_api.generate_reddit_api_token()
        headers = self.reddit_api.generate_headers(token)
        res = self.request_factory.get(url, headers=headers)

        is_valid: bool = False
        if res.status_code == 200:
            res_dict = json.loads(res.text)
            res_data = res_dict["data"]

            if res_data.get("url") is not None:
                logger.debug(
                    "SUBREDDIT {}: {}".format(subreddit, self.main_constants.check_mark_symbol))
                logger.info(
                    "Validating subreddit {}: {}".format(subreddit, self.main_constants.check_mark_symbol)) \
                    if verbose else None
                is_valid = True
            else:
                logger.debug(
                    "SUBREDDIT {}: {}".format(subreddit, self.main_constants.cross_symbol))
                logger.info(
                    "Validating {}: {}".format(subreddit, self.main_constants.cross_symbol)) if verbose else None
                is_valid = False
        return is_valid

    def validate_reddit_user(self, reddit_user: str, verbose: bool) -> Optional[bool]:
        """
        Checks if the given username exists on Reddit API.

        Args:
            reddit_user (str): The name of the user to check.
            verbose (bool): Controls the verbosity level

        Returns:
            bool: True if the user exists, False otherwise.

        Notes:
            According to Reddit's API rules changed the client's User-Agent string to something unique and descriptive,
            including the target platform, a unique application identifier, a version string, and your username
            as contact information, in the following format

            this check can also be accomplished by targeting this endpoint:
                url = "{constants.reddit_api_base_url}/api/v1/user/{username}/trophies"
        """

        url: str = "{}/api/username_available.json?user={}".format(
            self.main_constants.reddit_api_base_url, reddit_user)
        token = self.reddit_api.generate_reddit_api_token()
        headers = self.reddit_api.generate_headers(token)
        res = self.request_factory.get(url, headers=headers)

        exists: bool = False

        if res.status_code == 200:
            # If the enpoint returns False, it means the username isn't available and as such the user exists
            if res.json() is False:
                exists = True
                debug_msg = "USER {} EXISTS: {}".format(reddit_user, self.main_constants.check_mark_symbol)
                info_msg = "User: {}: {}".format(reddit_user,
                                                 self.main_constants.check_mark_symbol)
                logger.debug(debug_msg)
                logger.info(info_msg) if verbose else None
            else:
                debug_msg = "USER {} DOESN'T EXISTS: {}".format(reddit_user, self.main_constants.cross_symbol)
                info_msg = "User: {}: {}".format(reddit_user,
                                                 self.main_constants.cross_symbol)
                logger.debug(debug_msg)
                logger.info(info_msg) if verbose else None
                raise UserNotFoundException("Reddit user {} not Found".format(reddit_user))

        return exists
