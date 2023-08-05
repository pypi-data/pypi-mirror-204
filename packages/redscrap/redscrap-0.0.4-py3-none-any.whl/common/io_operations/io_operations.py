import glob
import json
import mimetypes
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from PIL import Image  # type: ignore
from loguru import logger  # type: ignore
from tqdm import tqdm

from common.constants.common_constants import CommonConstants  # type: ignore
from common.logging.logging_setup import LoggingSetup  # type: ignore


class IOOperations:
    """
    The IOOperations class provides methods for input-output operations, including writing detailed post information,
    validating directories, sorting files by MIME type and resolution, and deleting original files.

    This class requires access to the ConstantsNamespace and LoggingSetup classes from the common package, as well as
    the PIL library for image processing.

    Methods:
        - def write_detailed_post_information(payload: Any, operation: str, filename) -> None:
            Writes payload to a file with the given filename, using the specified operation mode. The file format is
            determined by the extension of the filename. output_post_detailed_information(payload): Writes all image
            URLs in payload to a JSON file named src/output/image_urls.json, sorted by subreddit and post.

        - def validate_directories(input_dir):
            Checks if the input_dir directory exists. If it does not exist, logs an
            error message and exits the program.

        - def sort_by_mime_type_and_resolution(input_dir: Path, output_dir: Path, remove: bool):
            Sorts all files in the input_dir directory by MIME type and resolution. The sorted files are copied to the
            corresponding folders in the output_dir directory, and original files are deleted if the remove flag is set
             to True.

        - def delete_original_files(input_dir, remove): Deletes all original files in the input_dir directory if the
        remove flag is set to True.
    """

    def __init__(self) -> None:
        super().__init__()
        self.logging_funcs = LoggingSetup()
        self.constants = CommonConstants()

    def validate_path_is_dir_and_exists(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                logger.debug("Valid file path but not directory")
                is_valid = False
            elif os.path.isdir(path):
                logger.debug("Valid directory path")
                is_valid = True
            else:
                logger.debug("Valid path, but not a file or directory")
                is_valid = False
        else:
            is_valid = False

        return is_valid

    def init_directory(self, path):
        """
        Checks if a directory exists at the given path and creates it if it does not exist.

        Args:
            path (str): The path to the directory to check/create.
        """
        if not os.path.exists(path):
            os.makedirs(path)
            msg = "Directory created at {}".format(path)
            logger.debug(msg)
        else:
            msg = "Directory already exists at {}".format(path)
            logger.debug(msg)

    def init_directories(self, output):

        if output is not None:
            validate_path_is_dir_and_exists = self.validate_path_is_dir_and_exists(output)
            if validate_path_is_dir_and_exists:
                logger.debug("Provided output parameter: {} is VALID".format(output))
                output_directory = output
            else:
                output_directory = output
        else:
            # Check if the Documents folder exists in the user's home directory. If not attempt to create it
            if os.name == 'nt':  # for Windows systems
                docs_folder = os.path.join(os.path.expanduser("~"), "Documents")
            else:  # for Linux and macOS systems
                docs_folder = os.path.join(os.path.expanduser("~"), "Documents")

            if os.path.exists(docs_folder):
                logger.debug("Documents folder exists at:", docs_folder)
            else:
                try:
                    logger.debug("Documents folder doesn't exist at: {}. \n Attempt to create it.".format(docs_folder))
                    output_directory = os.path.join(docs_folder, "output")
                    os.makedirs(output_directory)
                    logger.debug("Documents folder created at:", output_directory)
                except OSError as exc:
                    logger.error("Error creating Documents folder:", exc)
                    raise OSError("Error creating Documents folder:", exc)

            output_directory = os.path.join(docs_folder, "output")

        user_reports = os.path.join(output_directory,
                                    self.constants.user_reports_default_output_directory)
        subreddit_reports = os.path.join(output_directory,
                                         self.constants.subreddits_reports_default_output_directory)
        subreddit_downloads_directory = os.path.join(output_directory,
                                                     self.constants.subreddits_img_downloads_default_output_directory)
        user_downloads_directory = os.path.join(output_directory,
                                                self.constants.user_img_downloads_default_output_directory)
        logs = os.path.join(output_directory, self.constants.logs_default_output_directory)

        self.init_directory(output_directory)
        self.init_directory(user_reports)
        self.init_directory(subreddit_reports)
        self.init_directory(subreddit_downloads_directory)
        self.init_directory(user_downloads_directory)
        self.init_directory(logs)

        return output_directory

    def validate_directory(self, input_dir: str):
        """Check if the input directory exists and exit if it does not.

        Args:
            input_dir (str): The path to the input directory.
        """
        # Checking if input directory exists
        input_dir_path = Path(input_dir)
        if not input_dir_path.exists():
            logger.error("Input directory does not exist")
            sys.exit()

    #  @contextmanager decorator allows the image file to be opened and closed automatically
    @contextmanager
    def write_detailed_post_information(
            self, payload: Any, operation: str, filename: str, verbose: bool):
        """Write payload to a file in the specified format.

        Args:
            payload: The data to be written to the file.
            operation: The file operation mode ('w' for write, 'a' for append, etc.).
            filename: The path and filename of the file to write to.
            verbose: Boolean flag that controls the verbosity output
        """
        logger.debug("[9] STARTED WRITING SUBREDDIT REPORT INFORMATION STEP")

        extension = Path(filename).suffixes[-1]

        with open(filename, operation, encoding="utf-8") as file:
            if extension == ".txt":
                file.write(payload)
            elif extension == ".json":
                json_str = json.dumps(payload, indent=4)
                file.write(json_str)

        logger.info("Report written to {}".format(filename)) if verbose else None
        logger.debug("[9] FINISHED WRITING SUBREDDIT REPORT INFORMATION STEP")

    def create_output_folder_and_move_files(
            self, file_path: Path, output_dir: Path, matching_res: str, mimetype: str):
        """
        Creates the output folder and then moves the files to said folder
        Args:
            file_path (Path): Path to the file to be moved
            output_dir (Path): Path to the output directory
            matching_res (str): Matching resolution of the file
            mimetype (str): Mimetype of the file
        """
        destination_path = os.path.join(
            output_dir, matching_res, mimetype.split("/")[1]
        )

        os.makedirs(destination_path, exist_ok=True)
        shutil.copy2(file_path, destination_path)
        msg = "Copied {} to {}".format(file_path, destination_path)
        logger.debug(msg)

    def delete_original_files(self, input_dir: Path, remove: bool, verbose: bool):
        """Delete the original files from the input directory if `remove` is True.

        Args:
            input_dir (str): The path to the input directory.
            remove (bool): Whether to remove the original files.
            verbose (bool): Determines the level of verbosity
        """
        logger.debug("[8] STARTED CLEANUP STEP")
        if remove:
            input_dir_path = input_dir
            for file in input_dir_path.iterdir():
                if file.is_file():
                    file.unlink()

        logger.debug("[8] FINISHED CLEANUP STEP")

    def sort_by_mime_type_and_resolution(self, input_dir: Path, output_dir: Path, remove: bool, verbose):
        """Sort image files in the input directory by MIME type and resolution and save them to the
        output directory.

        Args:
            input_dir (Path): The path to the input directory.
            output_dir (Path): The path to the output directory.
            remove (bool): Whether to remove the original files.
            verbose (bool): Determines the level of verbosity
        """
        logger.debug("[7] STARTED FILE SORTING STEP")

        msg = "Sorting downloaded images"
        logger.info(msg) if verbose else None

        image_files = glob.glob(str(input_dir) + "/*.jpg") + glob.glob(str(input_dir) + "/*.png") + glob.glob(
            str(input_dir) + "/*.gif")

        if verbose:
            # Wrapping the loop with tqdm and customize the appearance of the progress bar
            with tqdm(
                    total=len(image_files),
                    desc="Sorting images",
                    ncols=100,
                    colour="green",
                    unit_scale=True,
                    dynamic_ncols=True) as pbar:

                for file_path in Path(input_dir).glob("*.*"):
                    self.sort_file(file_path, output_dir)
                    pbar.update(1)

        else:
            for file_path in Path(input_dir).glob("*.*"):
                self.sort_file(file_path, output_dir)

        logger.debug("[7] FINISHED FILE SORTING STEP")

        # if remove flag is passed delete the original files
        self.delete_original_files(input_dir, remove, verbose)

    def sort_file(self, file_path: Path, output_dir: Path):
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                mimetype, _ = mimetypes.guess_type(str(file_path))
                # checks if img path has a mimetype, and it starts with image/.*
                if mimetype and mimetype.startswith("image/"):
                    # match the resolution to the resolutions in the resolutions dict
                    matching_key = next(
                        (resolution for resolution in self.constants.resolutions.keys()
                         if resolution[0] <= width <= resolution[2] and
                         resolution[1] <= height <= resolution[3]), None)

                    # If any of resolutions match, save the img to the corresponding folder, if it doesn't
                    # save the image to an "other" folder
                    if matching_key:
                        matching_value = self.constants.resolutions[matching_key]

                        msg = "The corresponding resolution for the matching resolution {} is {}." \
                            .format(matching_key, matching_value)
                        logger.debug(msg)

                        self.create_output_folder_and_move_files(
                            file_path, output_dir, matching_value, mimetype)
                    else:
                        logger.debug("The resolution is not in the dictionary.")

                        self.create_output_folder_and_move_files(file_path, output_dir, "other", mimetype)

        except IOError as exc:
            logger.error("Error occurred while processing %s: %s", file_path, exc)