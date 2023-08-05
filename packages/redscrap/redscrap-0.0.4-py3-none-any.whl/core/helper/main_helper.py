import glob
from pathlib import Path
from typing import Any, Optional, List, Union

from bs4 import ResultSet
from loguru import logger  # type: ignore

from common.constants.common_constants import CommonConstants  # type: ignore
from common.constants.logging_constants import LoggingConstants  # type: ignore
from common.exceptions.main_exceptions import MissingRequiredParameter  # type: ignore
from common.io_operations.image_downloader import ImageDownloader  # type: ignore
from common.io_operations.io_operations import IOOperations  # type: ignore
from common.logging.loguru_setup import LoguruSetup  # type: ignore
from common.validations.parameter_validations import ParameterValidations  # type: ignore
from common.validations.reddit_api_validations import RedditApiValidations  # type: ignore
from core.api.reddit_api import RedditApi  # type: ignore
from core.scraper.scraper_helper import ScraperHelper  # type: ignore
from core.scraper.thread_scraper import ThreadScraper  # type: ignore


class MainHelper:
    """
    A class that provides helper functions for the main application.

    Methods:
        export_threads_detailed_information(user_or_subreddit: str, export_mode: str,
            threads_list: dict[str, dict[str, dict[str, Any] | ResultSet | Any] | Any], verbose: bool) -> None:
            Writes all the image URLs to a JSON file, sorted by subreddit and post.

        scrape_user(reddit_user: str, verbose: bool, number_results: int) -> None:
            Scrapes a Reddit user's submissions, downloads the images, and exports detailed thread information.

        scrape_subreddit(subreddits: Optional[List[str]], sorting_type: str, number_results: Optional[int],
            details: bool, verbose: bool) -> None:
            Scrapes posts and comments from a subreddit.
    """

    def __init__(self) -> None:
        super().__init__()
        self.parameter_validations = ParameterValidations()
        self.image_downloader = ImageDownloader()
        self.io_operations = IOOperations()
        self.log_constants = LoggingConstants()
        self.main_constants = CommonConstants()
        self.reddit_api = RedditApi(
            self.main_constants.client_id,
            self.main_constants.secret_token,
            self.main_constants.username,
            self.main_constants.password,
        )
        self.thread_scraper = ThreadScraper()
        self.reddit_api_validations = RedditApiValidations()
        self.scraper_helper = ScraperHelper()

    def export_threads_detailed_information(self,
                                            user_or_subreddit: Union[str, list[str]],
                                            export_mode: str,
                                            threads_list: dict[str, dict[str, dict[str, Any] | ResultSet | Any] | Any],
                                            output_directory: str,
                                            verbose: Optional[bool]) -> None:
        """Write all the img urls to a json file, sorted by subreddit and post.

        Args:
            output_directory (str): Directory to output thread detailed information
            user_or_subreddit (str): The name of the user or subreddit to export data for
            export_mode (str): The export mode, which can be "single", "multiple", or "user"
            threads_list (List[dict]): A list of dictionaries containing thread information
            verbose (Optional[bool]): Whether to print verbose output

        Returns:
            None
        """

        match export_mode:
            case "single":
                for subreddit in user_or_subreddit:
                    detailed_report = "{}/reports/subreddits/{}_{}_summary.{}".format(
                        output_directory, self.main_constants.current_date, subreddit, "json")
                    subreddit_threads_list = threads_list[subreddit]
                    self.io_operations.write_detailed_post_information(
                        subreddit_threads_list, "w", detailed_report, verbose)
            case "multiple":
                filename = ' '.join(map(str, user_or_subreddit)).replace(" ", "_")
                detailed_report = "{}/reports/subreddits/{}_{}_summary.{}".format(
                    output_directory, self.main_constants.current_date, filename, "json")
                self.io_operations.write_detailed_post_information(
                    threads_list, "w", detailed_report, verbose)
            case "user":
                detailed_report = "{}/reports/users/{}_{}_summary.{}".format(
                    output_directory, self.main_constants.current_date, user_or_subreddit, "json")
                self.io_operations.write_detailed_post_information(
                    threads_list, "w", detailed_report, verbose)

    def scrape_user(self, reddit_user: str, sort: str, number_results: int, output_directory: str,
                    verbose: Optional[bool]) -> None:
        """
        Scrape a Reddit user's submissions, download the images, and export detailed thread information.

        Args:
            reddit_user (str): The name of the Reddit user to scrape.
            sort:  (str): The type of posts to be scraped: hot, new, top
            verbose (Optional[bool]): Whether to print verbose output.
            output_directory: (str): Directory to output the downloaded files and reports
            number_results (int): The number of results to scrape.
        """
        user_reddit_profile_to_scrape = self.main_constants.user_profile_to_scrape

        if reddit_user is None and user_reddit_profile_to_scrape is not None:
            reddit_user = user_reddit_profile_to_scrape
        elif (reddit_user is not None and user_reddit_profile_to_scrape is not None or reddit_user is not None
              and user_reddit_profile_to_scrape is None):
            reddit_user = reddit_user
        else:
            msg = "Missing reddit username. If you want to scrape a user profile you must provide a reddit user"
            raise MissingRequiredParameter(msg)

        # validate reddit user
        is_user_valid = self.reddit_api_validations.validate_reddit_user(reddit_user, verbose)

        if is_user_valid:
            # Scrape user submissions
            user_threads = self.thread_scraper.scrape_threads(
                reddit_user, sort, "user", verbose,
                number_results if number_results is not None else self.main_constants.user_num_threads_to_scrape)

            # Downloads scraped img urls
            self.image_downloader.download_img_url_list(
                reddit_user, user_threads, "user", output_directory, verbose)

            img_output_dir = Path("{}/downloads/user/{}".format(output_directory, reddit_user))

            image_files = self.scraper_helper.get_list_of_img_files_in_dir(img_output_dir)

            # If the image list size is bigger than 0, sort the downloaded images by mime type and resolution
            if len(image_files) > 0:
                self.io_operations.sort_by_mime_type_and_resolution(
                    img_output_dir,
                    img_output_dir,
                    True,
                    verbose,
                )

            self.export_threads_detailed_information(reddit_user, "user", user_threads, output_directory, verbose)

        logger.info("Finished scraping threads for subreddits: {}".format(reddit_user)) if verbose else None

    def scrape_subreddit(self, subreddits: Union[str, List[str]], sorting_type: str, number_results: Optional[int],
                         details: bool, output_directory: str, verbose: bool) -> None:
        """
        Scrape posts and comments from a subreddit.

        Args:
            subreddits (List[str], optional): A list of subreddits to scrape. If None, the user's subreddits will
                    be used.
            sorting_type (str): A string indicating how to sort the posts. Valid values: 'hot', 'new', 'top',
                'controversial', 'rising'.
            number_results (int, optional): The maximum number of posts to scrape. If None, all posts will be scraped.
            details (bool): If True, exports detailed information about each post to a JSON file.
            output_directory: (str): Directory to output the downloaded files and reports
            verbose (bool): If True, displays logging information during the scraping process.
        """

        user_subreddits_list = self.main_constants.user_subreddits_list

        if subreddits is None and user_subreddits_list is not None:
            subreddits = user_subreddits_list
        elif subreddits is not None and user_subreddits_list is not None or subreddits is not None \
                and user_subreddits_list is None:
            subreddits = subreddits
        else:
            msg = "Missing subreddits. If you want to scrape a subreddit or multiple subreddits, provide one or " \
                  "multiple subreddits separated by a comma or semi-colon"
            raise MissingRequiredParameter(msg)

        # Validate Args
        subreddits = self.parameter_validations.validate_subreddits_parameter(subreddits)

        # Validate Subreddit
        self.reddit_api_validations.validate_subreddits_list(subreddits, verbose)

        subreddits_detailed_information_dict: dict = {}

        # Scrape threads and comments, extract image urls and downloads them
        for subreddit in subreddits:
            subreddit_threads_list = self.thread_scraper.scrape_threads(
                subreddit, sorting_type, "subreddit", verbose,
                number_results if number_results is not None else self.main_constants.user_num_threads_to_scrape)

            subreddits_detailed_information_dict = {**subreddits_detailed_information_dict,
                                                    **subreddit_threads_list}

            self.image_downloader.download_img_url_list(
                subreddit, subreddit_threads_list, "subreddit", output_directory, verbose)

            img_output_dir = Path("{}/downloads/subreddit/{}".format(output_directory, subreddit))

            image_files = glob.glob(str(img_output_dir) + "/*.jpg") + glob.glob(
                str(img_output_dir) + "/*.png") + glob.glob(
                str(img_output_dir) + "/*.gif")

            if len(image_files) > 0:
                self.io_operations.sort_by_mime_type_and_resolution(img_output_dir, img_output_dir, True, verbose)

        if details:
            self.export_threads_detailed_information(subreddits, "single", subreddits_detailed_information_dict,
                                                     output_directory, verbose)
        else:
            self.export_threads_detailed_information(subreddits, "multiple", subreddits_detailed_information_dict,
                                                     output_directory, verbose)

        logger.info("Finished scraping threads for subreddits: {}".format(" ".join(map(str, subreddits)))) \
            if verbose else None
