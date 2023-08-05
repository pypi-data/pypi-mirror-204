import glob
from contextlib import contextmanager
from pathlib import Path
from typing import List
from urllib.parse import urlparse
from loguru import logger  # type: ignore
from tqdm import tqdm
import httpx

from common.logging.utils.loguru_wrappers import logger_wraps  # type: ignore
from common.validations.url_validations import UrlValidations  # type: ignore
from common.constants.common_constants import CommonConstants  # type: ignore
from common.io_operations.io_operations import IOOperations  # type: ignore


class ImageDownloader:
    """
    The ImageDownloader class is used to download images from URLs.

    Methods:
        def download_img_url_list(self, subreddit_or_user, subreddit_or_user_threads_list, output_dir, log_mode,
         verbose):
             downloads an image from the given URL and saves it to a file with a filename inferred from the URL and the
             appropriate file extension. The method has three parameters: url, which is the URL of the image to
             download; verbose, which is a boolean indicating whether to print verbose output; and output_dir, which is
             the directory to save the downloaded image to. The default value for output_dir is the current directory.
        def download_img_urls_sync(self, scrapped_subreddit: str, subreddits_img_list: List[str], directory: str,
                               verbose: bool) -> None:
                                downloads the images from the URLs scrapped from a given subreddit. The method has
                                three parameters: scrapped_subreddit, which is the name of the subreddit from which the
                                URLs were scrapped; subreddits_list, which is a dictionary of subreddits and their
                                respective posts and URLs; and verbose, which is a boolean indicating whether to print
                                verbose output.
    """

    def __init__(self) -> None:
        super().__init__()
        self.url_validations = UrlValidations()
        self.constants = CommonConstants()
        self.io_operations = IOOperations()

    @logger_wraps()
    def download_img_url_list(self, subreddit_or_user, subreddit_or_user_threads_list, log_mode, output_directory,
                              verbose):
        """
        Downloads and sorts image URLs from a subreddit.

        Args:
            subreddit_or_user (str): The name of the subreddit.
            subreddit_or_user_threads_list (dict): A dictionary containing a list of subreddit posts.
            log_mode (str): Determines where to output the downloaded images
            verbose (bool): Whether to output verbose messages or not.
        """
        subreddit_thread_img_list = []

        for subreddit_ele in subreddit_or_user_threads_list.keys():
            for thread in subreddit_or_user_threads_list[subreddit_ele].keys():
                thread_urls = subreddit_or_user_threads_list[subreddit_ele][thread].get("urls")
                subreddit_thread_img_list = subreddit_thread_img_list + thread_urls
            if len(subreddit_thread_img_list) > 0:
                if log_mode == "subreddit":
                    output_dir = Path("{}/downloads/subreddit/{}".format(output_directory, subreddit_ele))
                else:
                    output_dir = Path("{}/downloads/user/{}".format(output_directory, subreddit_ele))

                self.download_img_urls_sync(subreddit_thread_img_list, output_dir, verbose)

        if log_mode == "subreddit":
            msg = "{} report: {} images scrapped for the subreddit {}".format(
                subreddit_or_user, len(subreddit_thread_img_list), subreddit_or_user)
        else:
            msg = "{} report: {} images scrapped".format(
                subreddit_or_user, len(subreddit_thread_img_list))
        logger.debug(msg)

    def download_img_urls_sync(self, subreddits_img_list: List[str], output_directory: Path, verbose: bool) -> None:
        """
        Downloads the images from the URLs scrapped from the given subreddit.

        Args:
            subreddits_img_list (List[str]): list of subreddits images
            output_directory (Path): Directory to output the downloaded images
            verbose (bool): Whether to print verbose output.
        """
        logger.debug("[6] STARTING IMAGE DOWNLOAD STEP")
        logger.info("Downloading scraped images") if verbose else None

        if not output_directory.exists():
            output_directory.mkdir(parents=True)

        # Make a GET request to the specified URL using httpx.
        transport = httpx.HTTPTransport(retries=3)
        client = httpx.Client(transport=transport)

        failed_urls = []
        downloaded_urls = []

        subreddits_img_list = list(set(subreddits_img_list))

        try:
            if verbose:
                # Wrapping the loop with tqdm and customize the appearance of the progress bar
                with tqdm(total=len(subreddits_img_list), desc="Downloading images", ncols=100, colour="green",
                          unit_scale=True, dynamic_ncols=True) as pbar:
                    for url in subreddits_img_list:
                        try:
                            response = client.get(url, timeout=10.0)  # Set a 10-second timeout

                            if response.status_code == 200:
                                self.download_img_url(url, response.read(), output_directory)
                                downloaded_urls.append(url)
                            else:
                                failed_urls.append(url)
                        except httpx.TimeoutException:
                            failed_urls.append(url)  # Add the URL to the failed_urls list if the request times out.

                        pbar.update(1)
            else:
                for url in subreddits_img_list:
                    try:
                        response = client.get(url, timeout=10.0)  # Set a 10-second timeout

                        if response.status_code == 200:
                            self.download_img_url(url, response.content, output_directory)
                            downloaded_urls.append(url)
                        else:
                            failed_urls.append(url)
                    except httpx.TimeoutException:
                        failed_urls.append(url)  # Add the URL to the failed_urls list if the request times out.
        finally:
            client.close()

        self.generate_download_report(output_directory, subreddits_img_list, downloaded_urls, failed_urls, verbose)

        logger.debug("[6] FINISHED IMAGE DOWNLOAD STEP")

    @contextmanager
    def download_img_url(self, url: str, payload: bytes, output_directory: Path):
        """
        Downloads an image from a URL to a specified directory.

        Args:
            url (str): The URL of the image to download.
            payload (bytes): The image file data.
            output_directory (Path): The output directory where the image will be saved.
        """
        # set the output file path
        output_file = output_directory / Path(urlparse(url).path).name

        msg = "Response: {}".format(self.constants.check_mark_symbol)
        logger.debug(msg)

        # If the response is ok and the output file doesn't exist, save it to it's destination
        if not output_file.exists():
            with open(output_file, "wb") as ifile:
                ifile.write(payload)
                msg = "{} - Downloaded {} to target folder {}".format(
                    self.constants.check_mark_symbol, url, output_file)
                logger.debug(msg)
        else:
            msg = "{} - Skipping: {} already exists in the target folder {}".format(
                self.constants.cross_symbol, url, output_directory)
            logger.debug(msg)

    @logger_wraps()
    def generate_download_report(self, output_dir: Path, subreddits_img_list: List[str],
                                 downloaded_urls: List[str], failed_urls: List[str], verbose: bool):
        """
        Generates report for the downloading process of the subreddits images

        Args:
            output_dir (Path): Output path
            subreddits_img_list (List[str]): List of images scraped from the subreddit
            failed_urls (List[str]): List of failed downloaded urls
            downloaded_urls (List[str]): List of successfully downloaded urls
            verbose: (bool): controls the verbosity level
        """
        image_files = glob.glob(str(output_dir) + "/*.jpg") + glob.glob(str(output_dir) + "/*.png") + glob.glob(
            str(output_dir) + "/*.gif")

        total_url_list_length = len(subreddits_img_list)
        failed_urls_length = len(subreddits_img_list) - len(image_files) \
            if (len(subreddits_img_list) - len(image_files)) > 0 else 0
        downloaded_urls_length = (total_url_list_length - failed_urls_length)

        info_msg = "From {} urls scrapped, {} urls where downloaded successfully and {} urls failed download".format(
            total_url_list_length, downloaded_urls_length, failed_urls_length)
        logger.info(info_msg) if verbose else None
        debug_msg = "Successful urls: {}, \n Failed urls: {}".format(downloaded_urls, failed_urls)
        logger.debug(debug_msg)
