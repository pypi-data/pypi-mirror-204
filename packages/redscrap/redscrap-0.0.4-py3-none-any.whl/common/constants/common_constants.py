import datetime
from collections import defaultdict
from pathlib import Path
import os


class CommonConstants:
    """
    A class that contains constants used throughout the application.

    Attributes:
        old_reddit_url (str): Old reddit base url.
        reddit_api_base_url (str): Reddit API base url.
        resolutions (defaultdict): Resolutions for the most popular resolutions.
        default_logger_format (str): Default logger format.
        default_logger_date_format (str): Default logger date format.
        attrs (dict): Default attributes for scraping reddit posts.
        possible_urls (list): Valid possible url prefixes that may appear during scraping.
        invalid_urls (list): Invalid possible url prefixes that may appear during scraping.
        match_url (str): Regex that match urls in the format https://subdomain.domain.
        domain_regex (str): Regex for validating domains.

    Properties:
        logs_default_output_directory (str): Logs default output directory.
        user_reports_default_output_directory (str): User reports default output directory.
        subreddits_reports_default_output_directory (str): Subreddits reports default output directory.
        user_img_downloads_default_output_directory (str): User image downloads default output directory.
        subreddits_img_downloads_default_output_directory (str): Subreddits default output directory.
        client_id (str): User API key.
        secret_token (str): User API secret.
        username (str): User Reddit username.
        password (str): User Reddit password.
        user_subreddits_list (str): Subreddit user list. A string of comma-separated subreddits.
        user_profile_to_scrape (str): Subreddit user list. A string of comma-separated subreddits.
        user_subreddits_sort_method (str): Subreddit user list sort method. A string of comma-separated subreddits.
        reddit_headers (dict): A dictionary containing the user agent header information.
        check_mark_symbol (str): Check mark symbol.
        cross_symbol (str): Cross symbol.
        reddit_url (str): New Reddit base URL.
        old_reddit_url (str): Old Reddit base URL.
        reddit_api_base_url (str): Reddit API base URL.
        output_path (Path): Output path for subreddits.
        resolutions (defaultdict): a dictionary containing a tuple of integers representing a resolution as the key and the
        corresponding resolution label as the value.
        user_agent (str): User agent information for Reddit.
    """

    @property
    def click_scrape_subreddits_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "Scrape subreddits threads"

    @property
    def click_scrape_user_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "Scrape user threads"

    @property
    def click_number_of_threads_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "Number of threads to scrape"

    @property
    def click_filter_threads_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "Filter threads"

    @property
    def click_details_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "If enable outputs the detailed list of threads of each subreddit provided into an individual file"

    @property
    def click_sorting_filter_option_help_msg(self):
        return "Thread sorting filter"

    @property
    def click_output_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "The directory to output the downloads"

    @property
    def click_verbose_option_help_msg(self):
        """
        Returns:
            (str): Logs default output directory.
        """

        return "Enables verbose mode"

    @property
    def logs_default_output_directory(self):
        """
        Returns:
            (str): Logs default output directory.
        """
        return "logs"

    @property
    def user_reports_default_output_directory(self):
        """
        Returns:
            (str): User reports default output directory.
        """
        return "reports/users"

    @property
    def subreddits_reports_default_output_directory(self):
        """
        Returns:
            (str): Subreddits reports default output directory.
        """
        return "reports/subreddits"

    @property
    def user_img_downloads_default_output_directory(self):
        """
        Returns:
            (str): user image downloads default output directory.
        """
        return "downloads/user"

    @property
    def subreddits_img_downloads_default_output_directory(self):
        """
        Returns:
            (str): subreddits default output directory.
        """
        return "downloads/subreddit"

    @property
    def client_id(self):
        """
        Returns:
            (str): User API key.
        """

        return os.environ.get("REDDIT_API_KEY")

    @property
    def secret_token(self):
        """
        Returns:
            (str): User API secret.
        """

        return os.environ.get("REDDIT_API_SECRET")

    @property
    def username(self):
        """
        Returns:
            (str): User reddit username.
        """

        return os.environ.get("REDDIT_USERNAME")

    @property
    def password(self):
        """
        Returns:
            (str): - User reddit password
        """

        return os.environ.get("REDDIT_PASSWORD")

    @property
    def user_subreddits_list(self):
        """
        Returns:
            (str): Subreddit user list. A string of comma separated subreddits.
        """

        return os.environ.get("SUBREDDITS_TO_SCRAPE")

    @property
    def user_profile_to_scrape(self):
        """
        Returns:
            (str): Subreddit user list. A string of comma separated subreddits.
        """

        return os.environ.get("REDDIT_USER_TO_SCRAPE")

    @property
    def user_num_threads_to_scrape(self):
        return os.environ.get("NUM_THREADS_TO_SCRAPE")

    @property
    def user_subreddits_sort_method(self):
        """
        Returns:
            (str): Subreddit user list sort method. A string of comma separated subreddits.
        """

        return os.environ.get("SUBREDDIT_SORT_METHOD")

    @property
    def reddit_headers(self):
        """
        Sets up the header info, which gives Reddit a brief description of the app.

        Returns:
            (dict): A dictionary containing the user agent header information.
        """

        return {
            "User-Agent": "Mozilla/5.0:com.martimdlima.redscrappy:v0.0.1 (by /u/mdlima__)"
        }

    @property
    def check_mark_symbol(self):
        """
        Returns:
            (str): Check mark symbol.
        """

        return "\N{CHECK MARK}"

    @property
    def cross_symbol(self):
        """
        Returns:
            (str): Cross symbol.
        """

        return "\N{BALLOT X}"

    @property
    def reddit_url(self):
        """
        Returns:
            (str): New Reddit base URL.
        """

        return "https://www.reddit.com"

    @property
    def old_reddit_url(self):
        """
        Returns:
            (str): Old Reddit base URL.
        """

        return "https://old.reddit.com"

    @property
    def reddit_api_base_url(self):
        """
        Returns:
            (str): Reddit API base URL.
        """

        return "https://oauth.reddit.com"

    @property
    def output_path(self):
        """
        Returns:
            (Path): Output path for subreddits.
        """

        return Path("./subreddit/")

    @property
    def resolutions(self):
        """
        Returns resolutions for the most popular resolutions.

        Returns:
            (defaultdict): a dictionary containing a tuple of integers representing a resolution as the key and the \
            corresponding resolution label as the value.
        """

        return defaultdict(
            lambda: "other",
            {
                (0, 0, 1280, 720): "720p",
                (1281, 721, 1920, 1080): "1080p",
                (1921, 1081, 2560, 1440): "1440p",
                (2561, 1441, 3840, 2160): "2160p",
                (3841, 2161, 7680, 4320): "4k",
                (7681, 4321, float("inf"), float("inf")): "8k",
            },
        )

    @property
    def user_agent(self):
        """
        Returns the User-Agent header for HTTP requests.

        Returns:
            (dict): a dictionary containing the User-Agent header.
        """

        return {"User-Agent": "Mozilla/5.0"}

    @property
    def attrs(self):
        """
        Returns the default attributes for scraping Reddit posts.

        Returns:
            (dict): a dictionary containing the default attributes.
        """

        return {"class": "thing"}

    @property
    def possible_urls(self):
        """
        Returns the valid possible URL prefixes that may appear during scraping.

        Returns:
            (list): a list of strings containing the valid URL prefixes.
        """

        return [
            "ze-robot.com/dl/",
            "preview.redd.it",
            "i.redd.it/",
            "static.greatbigcanvas.com",
            "external-preview.redd.it/"
            # "https://preview.redd.it/",
            # "https://ze-robot.com",
            # "https://i.redd.it/",
            # "https://old.reddit.com/r/",
            # "https://static.greatbigcanvas.com",
            # "https://external-preview.redd.it/"
        ]

    @property
    def invalid_url_prefixes(self):
        """
        Returns the invalid possible URL prefixes that may appear during scraping.

        Returns:
            (list): a list of strings containing the invalid URL prefixes.
        """

        return [
            "/u/ze-robot/",
            "https://ze-robot.com/#faq",
            "https://www.wallpaperflare.com/",
            "https://www.reddit.com/message/compose/",
            "https://old.reddit.com/user",
        ]

    @property
    def match_url(self):
        """
        Returns the regular expression that matches URLs in the format https://subdomain.domain.

        Returns:
            (str): a string containing the regular expression.
        """

        reg = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/[-\w./?%&=]*"
        return reg

    @property
    def replace_consecutive_commas_or_semicolons_regex(self):
        """
        Replace consecutive commas or semicolons with a single comma in a comma or semicolon separated string

        Returns:
            (str): a string containing the regular expression.
        """
        return r"[,;]+"

    @property
    def remove_empty_groups_from_comma_or_semicolon_separated_string(self):
        """
        Remove any remaining empty groups in a comma or semicolon separated string

        Returns:
            (str): a string containing the regular expression.
        """
        return r"(^,)|(,$)|(^;)|(;$)|,{2,}"

    @property
    def domain_regex(self):
        """
        Returns the regular expression for validating domains.

        The first regular expression uses a positive lookahead to assert that the string contains between 1 and 254
        characters ((?=^.{1,254}$)). Then it uses a capturing group to match one or more repetitions of a subpattern
        that consists of one or more characters that are not a digit followed by an optional dot.
        Finally, it uses a non-capturing group to match two or more
        alphabetical characters ((?:[a-zA-Z]{2,})$). In summary, this regex matches a string that consists of one
        or more non-digit characters followed by an optional dot, and ends with two or more alphabetical
        characters. This would match a domain name such as "example.com".

        The second regular expression is a simplified version of the first one, and it only matches domain names
        that consist of one or more subdomains separated by dots, followed by a top-level domain.
        The regex starts by using a capturing group to match one or more repetitions of a subpattern that consists
         of a letter or digit ([a-zA-Z0-9]), followed by an optional subpattern that consists of between 0 and 61
         characters that are either a letter, digit, or a hyphen (([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?),
         followed by a dot. This pattern is repeated one or more times, followed by a subpattern that matches
        two or more alphabetical characters ([a-zA-Z]{2,}). In summary, this regex matches a string that consists
        of one or more subdomains separated by dots, followed by a top-level domain. This would match a domain
        name such as "sub.example.com".

        Returns:
            (str): a string containing the regular expression.
        """

        # reg"(?=^.{1,254}$)(^(?:(?!\d+\.)[a-zA-Z0-9_\-]{1,63}\.?)+(?:[a-zA-Z]{2,})$)"
        reg = r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        return reg

    @property
    def path_regex(self):
        """
        Returns the regular expression for validating paths.

        Returns:
            (str): a string containing the regular expression.
        """

        return r"^\/[\/\.a-zA-Z0-9\-]+$"

    @property
    def path_regex_with_query_params(self):
        """
        Returns the regular expression for validating paths with query parameters.

        Returns:
            (str): a string containing the regular expression.
        """

        reg = r"^(\/\w+)+(\.)?\w+(\?(\w+=[\w\d]+(&\w+=[\w\d]+)*)+){0,1}$"
        return reg

    @property
    def validate_and_split_string_regex(self):
        """
        Validates if a string is composed of values separated by commas or semicolons and only contains plus signs,
        underscores, and alphanumeric characters.

        Returns:
            (str): A regular expression pattern that matches the validated string pattern.
        """

        # pattern = r'[^\w\s,;]+'
        # pattern = r"^[a-zA-Z0-9+\s]*([,;][a-zA-Z0-9+\s]*)*$"
        # pattern = ^[a-zA-Z0-9+\s]*([,;][a-zA-Z0-9+\s]*)*$

        # Check if the string contains any special characters besides commas and semicolons
        pattern = r"^[a-zA-Z0-9+_]*([,;][a-zA-Z0-9+_]*)*$"
        return pattern

    @property
    def extract_num_children(self):
        """
        Extracts decimal numbers from a string.

        Returns:
            (str): A regular expression pattern that matches decimal numbers.
        """

        pattern = r"\d+\.\d+|\d+"
        return pattern

    @property
    def current_date(self):
        """
        Returns the current date and time as a formatted string.

        Returns:
            (str): A formatted date string in the format: "dd_mm_yyyy_hh_mm_ss".
        """

        now = datetime.datetime.now()
        formatted_date = now.strftime("%d_%m_%Y_%H_%M_%S")
        return formatted_date
