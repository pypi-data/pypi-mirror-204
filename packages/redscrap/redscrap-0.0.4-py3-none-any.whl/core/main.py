import time
from pathlib import Path
from loguru import logger  # type: ignore
import click

from common.io_operations.io_operations import IOOperations  # type: ignore
from common.logging.loguru_setup import LoguruSetup  # type: ignore
from common.constants.logging_constants import LoggingConstants  # type: ignore
from common.constants.common_constants import CommonConstants  # type: ignore
from core.helper.main_helper import MainHelper  # type: ignore

logging_constants = LoggingConstants()
constants = CommonConstants()
io_operations = IOOperations()
main_helper = MainHelper()
main = click.Group(help="Reddit Scraper")


@main.command("user", help=constants.click_scrape_user_option_help_msg)
@click.argument('reddit_user', type=str, nargs=-1)
@click.option("-n", "--number_results", type=click.INT, help=constants.click_number_of_threads_option_help_msg)
@click.option("-s", "--sorting_filter", type=click.Choice(["top", "hot", "new"]), default="hot",
              help=constants.click_sorting_filter_option_help_msg)
@click.option("-o", "--output", type=str, help=constants.click_output_option_help_msg)
@click.option("-v", "--verbose", is_flag=True, default=False, help=constants.click_verbose_option_help_msg)
def main_scrape_user(number_results, sorting_filter, reddit_user, output, verbose):

    if number_results <= 0:
        raise click.BadParameter('Number must be bigger than zero.')

    # Setups directories used in the application
    with logger.catch(reraise=True):
        logger.remove()
        output_directory = io_operations.init_directories(output)

    # Setups logging for the application
    LoguruSetup.script_logger_config_dict(
        logger,
        output_directory,
        Path(logging_constants.log_filename).name,
        logging_constants.default_log_stfout_level,
        logging_constants.default_log_format,
        logging_constants.default_log_colorizing,
        logging_constants.default_log_rotation,
        logging_constants.default_log_retention,
        logging_constants.default_log_compression,
        logging_constants.default_log_delay,
        logging_constants.default_log_mode,
        logging_constants.default_log_buffering,
        logging_constants.default_log_encoding,
        logging_constants.default_log_serialize,
        logging_constants.default_log_backtrace,
        logging_constants.default_log_diagnose,
        logging_constants.default_log_enqueue,
        logging_constants.default_log_catch,
        False,  # enables/disables debug mode logs
    )

    s = time.perf_counter()

    main_helper.scrape_user(
        "".join(reddit_user) if len(reddit_user) > 0 else None,
        sorting_filter, number_results, output_directory, verbose)

    elapsed = time.perf_counter() - s
    logger.info(f"{__file__} executed in {elapsed:0.2f} seconds.")


@main.command("subreddits", help=constants.click_scrape_subreddits_option_help_msg)
@click.argument('subreddits', type=str, nargs=-1)
@click.option("-n", "--number_results", type=click.INT,
              help=constants.click_number_of_threads_option_help_msg)
@click.option("-s", "--sorting_filter", type=click.Choice(["top", "hot", "new"]), default="hot",
              help=constants.click_sorting_filter_option_help_msg)
@click.option("-d", "--details", is_flag=True, default=False,
              help=constants.click_details_option_help_msg)
@click.option("-o", "--output", type=str, help=constants.click_output_option_help_msg)
@click.option("-v", "--verbose", is_flag=True, default=False, help=constants.click_verbose_option_help_msg)
def main_scrape_subreddits(number_results, sorting_filter, subreddits, details, output, verbose):

    if number_results <= 0:
        raise click.BadParameter('Number must be bigger than zero.')

    # Setups directories used in the application
    with logger.catch(reraise=True):
        logger.remove()
        output_directory = io_operations.init_directories(output)

    # Setups logging for the application
    LoguruSetup.script_logger_config_dict(
        logger,
        output_directory,
        Path(logging_constants.log_filename).name,
        logging_constants.default_log_stfout_level,
        logging_constants.default_log_format,
        logging_constants.default_log_colorizing,
        logging_constants.default_log_rotation,
        logging_constants.default_log_retention,
        logging_constants.default_log_compression,
        logging_constants.default_log_delay,
        logging_constants.default_log_mode,
        logging_constants.default_log_buffering,
        logging_constants.default_log_encoding,
        logging_constants.default_log_serialize,
        logging_constants.default_log_backtrace,
        logging_constants.default_log_diagnose,
        logging_constants.default_log_enqueue,
        logging_constants.default_log_catch,
        False,  # enables/disables debug mode logs
    )

    s = time.perf_counter()

    main_helper.scrape_subreddit(
        ", ".join(subreddits) if len(subreddits) > 0 else None
        , sorting_filter, number_results, details, output_directory, verbose)

    elapsed = time.perf_counter() - s
    logger.info(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    exit(main())  # pylint: disable=no-value-for-parameter

