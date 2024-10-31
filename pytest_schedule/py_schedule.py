import argparse
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
import dpath
from loguru import logger

__version__ = "0.0.8"

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    filename="./pytest_schedule.log",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
)


def update_format_logger(color: str = "white"):
    """Update logger format."""
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
    """Run tests by schedule."""
    slots = {}
    time_intervals = []
    regex_time = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")

    def update_slots(local_tag: str):
        """Update slots by tag."""
        nonlocal slots
        with open("pytest_schedule.json", "r") as file:
            data = json.load(file)
        slots_by_tag = dpath.values(data, f"{__version__}/*/{local_tag}")
        _ = [slot[0] for slot in slots_by_tag if slots.update(slot[0])]
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
                            else:
                                update_format_logger(color="red")
                                logger.info(
                                    f"\t'{args.test_module}' test_module not existing!"
                                )
                                return
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
                                color=(
                                    "green"
                                    if test_result == " [PASSED]"
                                    else "red"
                                )
                            )
                            logger.info(
                                f"\t ({i}) {tag}::{test_name}::{time_} task completed  {test_result}"
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
    else:
        update_format_logger(color="red")
        logger.info(f"\t'{tag}' tag not existing!")
