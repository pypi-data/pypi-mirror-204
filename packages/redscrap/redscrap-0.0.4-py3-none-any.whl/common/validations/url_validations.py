from typing import List, Optional
import re
import validators  # type: ignore
from loguru import logger  # type: ignore

from common.logging.logging_setup import LoggingSetup  # type: ignore
from common.constants.common_constants import CommonConstants  # type: ignore

logging_setup = LoggingSetup()
constants = CommonConstants()


class UrlValidations:
    """
    A class that provides methods for validating URLs.

    Methods:
        - def validate_if_url_is_a_valid_img_link(self, url: str, possible_base_urls: List[str]) -> Optional[bool]:
            This method extracts the URL from the given string that contains one of the possible base URLs.
        - def validate_image_url(self, possible_base_urls: List[str], provided_url: str) -> bool:
            This method validates if any of the URLs in a URL list is equal or starts with a provided URL.

    """

    def __init__(self) -> None:
        super().__init__()

    def validate_if_url_is_a_valid_img_link(self, url: str, possible_base_urls: List[str]) -> Optional[bool]:
        """
        This method extracts the URL from the given string that contains one of the possible base URLs.

        Args:
            url (str): The string to check and extract from.
            possible_base_urls (list): A list of possible base URLs that the extracted URL might contain.

        Returns:
            bool: True if the given string contains a URL that contains one of the possible base URLs, or False
            otherwise.
        """
        pattern = rf'https?://(?:www\.)?(?:{"|".join(possible_base_urls)})[^\s]+'
        match = re.search(pattern, url)

        is_valid = None

        if match:
            if (match.group(0) != "/u/ze-robot"
                    and not match.group(0).startswith("https://old.reddit.com/r/")
                    and not match.group(0).startswith("old.reddit.com/r/")
                    and not match.group(0).startswith("https://old.reddit.com/user/")
                    and not match.group(0).startswith("old.reddit.com/user/")
                    and not match.group(0).startswith("https://ze-robot.com/#faq")
                    and not match.group(0).startswith("https://old.reddit.com/user")
                    and not match.group(0).startswith("https://www.wallpaperflare.com/")
                    and not match.group(0).startswith("https://www.reddit.com/r/")
                    and not match.group(0).startswith("http://www.wolframalpha.com/")
                    and not match.group(0).startswith("https://www.etsy.com/")
                    and not match.group(0).startswith("https://www.reddit.com/message/compose/")
                    and not match.group(0).startswith("imgur.com/")):
                is_valid = True
            else:
                is_valid = False

        return is_valid

    def validate_image_url(self, possible_base_urls: List[str], provided_url: str) -> bool:
        """
        This method validates if any of the URLs in a URL list is equal or starts with a provided URL.

        Args:
            possible_base_urls (list): A list of URLs to check.
            provided_url (str): The URL to compare against.

        Returns:
            bool: True if any of the URLs in the list is equal or starts with the provided URL, else False.
        """
        for url in possible_base_urls:
            if provided_url.startswith(url):
                return True
        return False
