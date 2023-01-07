from distutils.cmd import Command
from setuptools import setup
from setuptools.command.install import install
import glob
import json
import os

__version__ = "0.0.6"


class GenerateSchedule(Command):
    description = "Generate pytest schedule json file."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self, directory: str = "./"):
        files = glob.glob(f"{directory}/**/*test*.py", recursive=True)
        contains = lambda path, file_name: os.path.basename(path).startswith(file_name)
        file_names = [
            {"tag": [{os.path.basename(path): "time"}]}
            for path in files
            if not contains(path, "conftest") and not contains(path, "pytest")
        ]
        with open("./pytest_schedule.json", "w") as file:
            json.dump({__version__: file_names}, file, indent=2)
            print("finished schedule_json")


class InstallCommand(install):
    def run(self):
        self.run_command("schedule_json")
        return super().run()


setup(
    cmdclass={
        "schedule_json": GenerateSchedule,
        "install": InstallCommand,
    },
)
