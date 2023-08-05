import time
from typing import Any, Optional, Dict, Union, List, Tuple
from loguru import logger  # type: ignore
from bs4 import BeautifulSoup, ResultSet

from common.exceptions.main_exceptions import TokenErrorException  # type: ignore
from common.logging.logging_setup import LoggingSetup  # type: ignore
from common.constants.common_constants import CommonConstants  # type: ignore
from common.logging.utils.loguru_wrappers import logger_wraps   # type: ignore
from common.validations.url_validations import UrlValidations  # type: ignore
from common.io_operations.image_downloader import ImageDownloader  # type: ignore
from common.io_operations.io_operations import IOOperations  # type: ignore
from core.scraper.comment_scraper import CommentScraper  # type: ignore
from core.api.reddit_api import RedditApi  # type: ignore
from core.scraper.scraper_helper import ScraperHelper  # type: ignore
from common.io_operations.request_factory import RequestFactory     # type: ignore


class ThreadScraper:
    """
    A class that provides methods to scrape threads from subreddits or users

    Methods:
        - def scrape_threads(self, subreddit_or_user: str, sort: str, scrape_mode: str, verbose: bool,
            max_counter: Optional[int] = None ) -> Dict[str, Union[Dict[str, Union[Dict[str, Any], Dict[str, Any],
            ResultSet[Any], Dict[str, Any], Any]], Any]]:
            Scrape threads from a subreddit or user and return the results.

        - def scrape_single_thread(self, link: str, verbose: bool):
            Scrapes the given Reddit thread URL and returns a tuple containing a list of image URLs and a dictionary of
            comments.
    """

    def __init__(self) -> None:
        super().__init__()
        self.logging_funcs = LoggingSetup()
        self.constants = CommonConstants()
        self.validations = UrlValidations()
        self.comment_scrapper = CommentScraper()
        self.io_operations = IOOperations()
        self.image_downloader = ImageDownloader()
        self.scraper_helper = ScraperHelper()
        self.request_factory = RequestFactory()
        self.reddit_api = RedditApi(self.constants.client_id, self.constants.secret_token, self.constants.username,
                                    self.constants.password)

    @logger_wraps()
    def scrape_threads(self, subreddit_or_user: str, sort: str, scrape_mode: str, verbose: bool, max_counter: int
                       ) \
            -> Dict[
                str, Union[Dict[str, Union[Dict[str, Any], Dict[str, Any], ResultSet[Any], Dict[str, Any], Any]], Any]]:
        """
        Scrape threads from a subreddit or user and return the results.

        Args:
            subreddit_or_user (str): The name of the subreddit or user from which to scrape threads.
            sort (str): The method to sort the threads, such as "hot" or "top".
            scrape_mode (str): The mode in which to scrape threads, either "subreddit" or "user".
            verbose (bool): A flag indicating whether to log verbose output.
            max_counter (Optional[int], optional): The maximum number of threads to scrape.

        Returns:
            Dict[str, Union[ Dict[str, Union[Dict[str, Any], Dict[str, Any], ResultSet[Any], Dict[str, Any], Any]],
                Any]]:
                A dictionary of thread URLs and their corresponding information, such as their author, datetime,
                 rating, URLs, and comments.
        """
        params: Optional[Dict[str, Any]] = None

        if scrape_mode == "subreddit":
            endpoint = "/r/{}/{}/".format(subreddit_or_user, sort)
            url = "{}{}".format(self.constants.old_reddit_url, endpoint)
        else:
            # Generating the URL leading to the desired subreddit
            endpoint = "/user/{}/{}".format(subreddit_or_user, "submitted")
            url = "{}{}".format(self.constants.old_reddit_url, endpoint)
            params = self.reddit_api.generate_params_for_reddit_api_req(None, None, None, None, "all", None)

        req = self.request_factory.get(url, headers=self.constants.user_agent,
                                       params=params if params is not None else None)

        threads_urls: Dict[
            str, Union[Dict[str, Union[Dict[str, Any], Dict[str, Any], ResultSet[Any], Dict[str, Any], Any]], Any]
        ] = {}  # noqa comments
        thread_img_urls = {}

        counter = 1
        full = False
        if req.status_code == 200:
            msg = "\nCollecting information for {}....".format(url)
            logger.info(msg) if verbose else None

            soup: BeautifulSoup = BeautifulSoup(req.text, "html.parser")

            threads = self.scraper_helper.define_threads_based_on_search_parameter(scrape_mode, req, subreddit_or_user)

            max_count = int(max_counter)

            while full is not True:
                for thread in threads:
                    try:
                        msg = "\nCollecting information from thread {} of {}...".format(counter, max_count)
                        logger.info(msg) if verbose else None

                        thread_details_path = thread.attrs["data-permalink"]
                        thread_url = self.constants.old_reddit_url + thread_details_path
                        thread_comments, img_urls = self.scrape_single_thread(thread_details_path, verbose)
                        current_thread = "{}".format(thread_url)

                        thread_img_urls[current_thread] = {
                            "author": self.scraper_helper.construct_author_dict(thread),
                            "datetime": self.scraper_helper.construct_time_dict(thread),
                            "rating": self.scraper_helper.construct_thread_rating_dict(thread),
                            "thread_url": thread_url,
                            "urls": img_urls,
                            "comments": thread_comments
                        }

                        msg = "Finished scrapping images for thread {}. {} images where scraped".format(
                            thread_url, len(list(set(img_urls))))
                        logger.info(msg) if verbose else None

                        if counter == max_count:
                            full = True
                            break
                        time.sleep(2)
                        counter += 1
                    except AttributeError:
                        continue
                if full:
                    break

                try:
                    next_button = soup.find("span", class_="next-button")
                    if next_button is not None:
                        next_page_link = next_button.find("a").attrs["href"]  # type: ignore
                    else:
                        full = True
                        break

                    req = self.request_factory.get(next_page_link, headers=self.constants.user_agent)
                    soup = BeautifulSoup(req.text, "html.parser")
                except TokenErrorException as exc:
                    logger.exception(str(exc))
                    break

            threads_urls[subreddit_or_user] = thread_img_urls

            logger.debug("[5] FINISHED SCRAPING STEP")
        else:
            message = "Error fetching results.. Try again!"
            logger.exception(message, verbose)

        return threads_urls

    def scrape_single_thread(self, link: str, verbose: bool) -> Tuple[list[dict[str, Any]], list[str]]:
        """
        Scrapes the given Reddit thread URL and returns a tuple containing a list of image URLs and a dictionary of
        comments.

        Args:
            link (str): The URL of the Reddit thread to be scraped.
            verbose (bool): Whether to print verbose logging messages.

        Returns:
            Tuple[List[str], Dict[str, Dict[str, Any]]]:
                A tuple containing a list of image URLs and a dictionary of
                comments. The first element of the tuple is a list of strings representing image URLs, and the second
                element is a dictionary of comments. The dictionary has keys that correspond to the comment IDs and
                values that are dictionaries containing information about each comment.
        """

        msg = "Scraping thread: {}{}".format(self.constants.old_reddit_url, link)
        logger.info(msg) if verbose else None

        # Using a user-agent to mimic browser activity
        req = self.request_factory.get(self.constants.old_reddit_url + link, headers=self.constants.user_agent)

        # Parsing through the web page for obtaining the right html tags
        # and scraping the details required
        soup: BeautifulSoup = BeautifulSoup(req.text, "html.parser")

        thread_images: List[str] = []

        thread_img_ele = soup.find("div", attrs={"class", "expando"})

        self.scraper_helper.process_thread_images(thread_img_ele, thread_images)
        thread_comments, img_urls = self.comment_scrapper.scrape_comments(soup)

        thread_images = list(set(thread_images))

        # Remove all elements from thread_images that contain the value "crop=smart"
        thread_images = [x for x in thread_images if "crop=smart" not in x]
        img_urls = img_urls + thread_images

        return thread_comments, img_urls
