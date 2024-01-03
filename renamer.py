"""
Renamer

Usage:
    renamer.py rename-files --directory=<directory> --pattern=<pattern> --replacement=<replacement> [--recursive] [--ignore-folders=<ignore_folders>] [--dry-run] [--verbose]
    renamer.py rename-strings --directory=<directory> --pattern=<pattern> --replacement=<replacement> [--recursive] [--ignore-folders=<ignore_folders>] [--dry-run] [--verbose]
    renamer.py (-h | --help)

Options:
    -h --help                   Show this help message and exit.
    --directory=<directory>     The directory path where renaming operations will be performed.
    --pattern=<pattern>         The pattern to search for in file names or content.
    --replacement=<replacement> The replacement string for the specified pattern [default: ''].
    --recursive                 Perform renaming operations recursively in nested directories
    --ignore-folders=<ignore_folders>   Comma-separated list of folder names to ignore during renaming [default: ''].
    --dry-run                   Perform a dry run without actually making changes
    --verbose                   Enable verbose mode for debugging

Commands:
    rename-files               Rename files in the specified directory based on the given pattern.
    rename-strings             Rename strings within files in the specified directory based on the given pattern.

Example:
    renamer.py rename-files --directory=/path/to/directory --pattern=ABC_ --replacement=A --recursive --ignore-folders=ignore_folder1,ignore_folder2 --verbose
    renamer.py rename-strings --directory=/path/to/directory --pattern=ABC --replacement=XYZ --recursive --ignore-folders=ignore_folder1,ignore_folder2 --verbose
"""

import os
import sys
import fnmatch
import re
import logging


class Renamer:
    def __init__(self, args):
        self.directory = args["--directory"]
        self.pattern = args["--pattern"]
        self.replacement = args["--replacement"]

        self.verbose = False

        self.ignore_folders = (
            args["--ignore-folders"].split(",") if args["--ignore-folders"] else []
        )
        self.recursive = args["--recursive"]
        self.dry_run = True if args["--dry-run"] else False
        self.verbose = args["--verbose"]

        self.logger = self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger("Renamer")
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        # # Log to console
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(levelname)s - %(message)s')
        # console_handler.setFormatter(formatter)
        # self.logger.addHandler(console_handler)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s] - %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)
        return self.logger

    def is_folder_ignored(self, folder_name):
        self.logger.debug("Processing")
        return folder_name in self.ignore_folders

    def rename_files(self):
        self.logger.debug("Processing")
        try:
            for root, dirs, files in os.walk(self.directory):
                dirs[:] = [d for d in dirs if not self.is_folder_ignored(d)]
                for filename in fnmatch.filter(files, f"*{self.pattern}*"):
                    old_path = os.path.join(root, filename)
                    new_filename = filename.replace(self.pattern, self.replacement)
                    new_path = os.path.join(root, new_filename)

                    self.logger.debug(f"Renaming file: {old_path} -> {new_path}")

                    if not self.dry_run:
                        os.rename(old_path, new_path)
        except Exception as e:
            self.logger.error(f"An error occurred during file renaming: {e}")
            sys.exit(1)

    def rename_strings(self):
        self.logger.debug("Processing")
        try:
            for root, dirs, files in os.walk(self.directory):
                dirs[:] = [d for d in dirs if not self.is_folder_ignored(d)]
                for filename in fnmatch.filter(files, "*.*"):
                    file_path = os.path.join(root, filename)

                    with open(file_path, "r") as file:
                        content = file.read()

                    new_content = re.sub(self.pattern, self.replacement, content)

                    if new_content != content:
                        self.logger.debug(f"Updating file: {file_path}")

                        if not self.dry_run:
                            with open(file_path, "w") as file:
                                file.write(new_content)
        except Exception as e:
            self.logger.error(f"An error occurred during string renaming: {e}")
            sys.exit(1)

    def run_command(self):
        self.logger.debug("Processing")
        if args["rename-files"]:
            self.rename_files()
        elif args["rename-strings"]:
            self.rename_strings()


if __name__ == "__main__":
    from docopt import docopt

    args = docopt(__doc__)

    renamer = Renamer(args)
    renamer.run_command()
