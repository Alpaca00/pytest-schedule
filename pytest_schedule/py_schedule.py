"""
The job of test scheduling for humans.

Usage:
Generate the tree of test module names recursively to root directory of "pytest_schedule.json"
$ python -m pytest_schedule.generate schedule_json

Run tests by any custom tags from "pytest_schedule.json"
$ python -m pytest_schedule -t tag
OR
$ python -m pytest_schedule --tags unittest,api,integration
OR
$ python -m pytest_schedule --tag unittest --test_module unittest
OR
$ python -m pytest_schedule --tag unittest --test_module pytest

The following options are available by the command:
$ python -m pytest_schedule --help
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

__version__ = "0.0.2"
__author__ = "Oleg Matskiv <alpaca00tuha@gmail.com>"
__status__ = "production"
__date__ = "05 January 2023"


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    filename="./pytest_schedule.log",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
)
new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")

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
        logger.log("SNAKY", f"\t\tThe job process started.")
        logging.debug(f" The job process started.")
        for test_name, time_ in slots.items():
            if bool(regex_time.match(time_)):
                time_now = lambda: datetime.now().strftime("%H:%M:%S")
                if time_ > time_now() or time_ in time_intervals:
                    time_intervals.append(time_)
                    logger.log(
                        "SNAKY",
                        f"\tWaiting job process of '{test_name}::{time_}' by '{tag}'.",
                    )
                    while time_now() != time_:
                        pass
                    else:
                        subprocess_result = None
                        try:
                            logger.log(
                                "SNAKY",
                                f"\tThe task process of '{test_name}::{time_}' by '{tag}' started.",
                            )
                            if args.test_module == "pytest":
                                subprocess_result = subprocess.run(
                                    [args.test_module, "-k", test_name], capture_output=True
                                )
                            elif args.test_module == "unittest":
                                subprocess_result = subprocess.run(
                                    [args.test_module, "-k", test_name], capture_output=True
                                )
                            logging.debug(
                                f" The task process of '{test_name}::{time_}' by '{tag}' started."
                            )
                            short_summary = re.findall(
                                r"FAILED.*", subprocess_result.stdout.decode("utf-8")
                            )
                            logging.debug(
                                f"{' [FAILED]' if short_summary else ' [PASSED]'}"
                            )
                        except KeyboardInterrupt:
                            logging.debug(f"\n{subprocess_result.stderr.decode('utf-8')}")
                            sys.exit(0)
                        finally:
                            logging.debug(
                                f" The task process of '{test_name}::{time_}' by '{tag}' finished."
                            )
                            logger.log(
                                "SNAKY",
                                f"\tThe task process of '{test_name}::{time_}' by '{tag}' finished.",
                            )
                else:
                    logging.debug(
                        f" {tag} contains not actual time and the job process will be skipped."
                    )
            else:
                logging.debug(
                    f" {tag} contains the default value 'time' and the job process will be skipped."
                )
        else:
            logger.log("SNAKY", "\tThe job process finished.")
            logging.debug(" The job process finished.")
