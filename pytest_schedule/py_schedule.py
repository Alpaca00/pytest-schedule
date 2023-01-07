"""
The job of test scheduling for humans.

You should to install the Pytest library if it's not already installed
$ pip install pytest

Usage:

Generate a tree of test module names, recursively, for the root directory of pytest_schedule.json
$ python -m pytest_schedule.generate schedule_json

Run tests with any custom tags from pytest_schedule.json
$ python -m pytest_schedule -t tag
$ python -m pytest_schedule --tags unittest,api,integration
$ python -m pytest_schedule --tag unittest --test_module unittest
$ python -m pytest_schedule --tag unittest --test_module pytest

The following options are available by the command:
$ python -m pytest_schedule --help

Change the time to 00:00:00 according to the template in the pytest_schedule.json file
{
  "0.0.4": [
    {
      "smoke": [
        {
          "test_binary_tree_0.py": "10:15:00"
        }
      ]
    },
    {
      "smoke": [
        {
          "test_module_binary_tree_1_0.py": "10:10:00"
        }
      ]
    },
    {
      "tag": [
        {
          "test_module_binary_tree_2_0_0.py": "time"
        }
      ]
    },
    ...
}
"""

import argparse
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
import dpath
from loguru import logger


__version__ = "0.0.5"
__author__ = "Oleg Matskiv <alpaca00tuha@gmail.com>"
__status__ = "production"
__date__ = "05 January 2023"

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    filename="./pytest_schedule.log",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
)


def update_format_logger(color: str = "white"):
    logger.remove()
    style = {
        "white": "<yellow>[{time:HH:mm:ss!UTC}] | PYTEST-SCHEDULE |</yellow> <white>{message}</white>",
        "yellow": "<yellow>[{time:HH:mm:ss!UTC}] | PYTEST-SCHEDULE |</yellow> <yellow>{message}</yellow>",
        "red": "<yellow>[{time:HH:mm:ss!UTC}] | PYTEST-SCHEDULE |</yellow> <red>{message}</red>",
        "green": "<yellow>[{time:HH:mm:ss!UTC}] | PYTEST-SCHEDULE |</yellow> <green>{message}</green>",
    }
    logger.add(sys.stdout, format=style[color])


arg = argparse.ArgumentParser()
arg.add_argument(
    "-t",
    "--tag",
    action="store",
    dest="tag",
    default=None,
    help="run tests by only one tag from 'pytest_schedule.json'",
)
arg.add_argument(
    "--tags",
    action="store",
    dest="tags",
    default=None,
    help="run tests by tags from 'pytest_schedule.json'",
)
arg.add_argument(
    "--test_module",
    action="store",
    dest="test_module",
    default="pytest",
    help="pytest and unittest test execution tools are available",
)

arguments = arg.parse_args()


def schedule(args: arguments):
    slots = {}
    time_intervals = []
    regex_time = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")

    def update_slots(local_tag: str):
        nonlocal slots
        with open("pytest_schedule.json", "r") as file:
            data = json.load(file)
        # # an array of all values which match the tag
        slots_by_tag = dpath.values(data, f"{__version__}/*/{local_tag}")
        # update dictionary of test module name and schedule time
        [slot[0] for slot in slots_by_tag if slots.update(slot[0])]
        # sorted by schedule time of slots dictionary
        slots = dict(sorted(slots.items(), key=lambda item: item[1]))

    if tag := args.tag:
        update_slots(tag)

    if tags := args.tags:
        for tag in tags.split(","):
            update_slots(tag)
    if slots:
        time_now = lambda: datetime.now().strftime("%H:%M:%S")

        update_format_logger(color="yellow")
        logger.info(f"\tThe job process started.")
        logging.debug(f" The job process started.")

        for i, (test_name, time_) in enumerate(slots.items(), start=1):
            if bool(regex_time.match(time_)):
                if time_ > time_now() or time_ in time_intervals:
                    time_intervals.append(time_)

                    update_format_logger()
                    logger.info(
                        f"\t ({i}) {tag}::{test_name}::{time_} task waiting .."
                    )

                    while time_now() != time_:
                        pass
                    else:
                        subprocess_result = None
                        try:
                            if args.test_module == "pytest":
                                subprocess_result = subprocess.run(
                                    [args.test_module, "-k", test_name],
                                    capture_output=True,
                                )
                            elif args.test_module == "unittest":
                                subprocess_result = subprocess.run(
                                    [args.test_module, "-k", test_name],
                                    capture_output=True,
                                )

                            update_format_logger()
                            logging.debug(
                                f"\t  ({i}) {tag} :: {test_name} :: {time_} task started"
                            )
                            logger.info(
                                f"\t ({i}) {tag}::{test_name}::{time_} task started .."
                            )

                            short_summary = re.findall(
                                r"FAILED.*",
                                subprocess_result.stdout.decode("utf-8"),
                            )
                            test_result = (
                                f"{' [FAILED]' if short_summary else ' [PASSED]'}"
                            )

                            logging.debug(
                                f"\t  ({i}) {tag} :: {test_name} :: {time_} task completed  {test_result}"
                            )
                            update_format_logger(
                                color="green"
                                if test_result == " [PASSED]"
                                else "red"
                            )
                            logger.info(
                                f"\t ({i}) {tag}::{test_name}::{time_} task completed  {test_result if test_result == ' [PASSED]' else test_result}"
                            )
                        except KeyboardInterrupt:
                            logging.debug(
                                f"\n{subprocess_result.stderr.decode('utf-8')}"
                            )
                            sys.exit(0)
                else:
                    logging.debug(
                        f" {tag} contains not actual time and the job process will be skipped."
                    )
            else:
                logging.debug(
                    f" {tag} contains the default value 'time' and the job process will be skipped."
                )
        else:
            update_format_logger(color="yellow")
            logger.info("\tThe job process finished.")
            logging.debug(" The job process finished.")
