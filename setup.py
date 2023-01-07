import io
import os
from pip._internal.req import parse_requirements
from setuptools import setup

__version__ = "0.0.6"


setup(
    author="Oleg Matskiv",
    author_email="alpaca00tuha@gmail.com",
    name="pytest-schedule",
    packages=["pytest_schedule"],
    package_data={"pytest_schedule": ["py_schedule.py"]},
    version=__version__,
    description="The job of test scheduling for humans.",
    long_description=io.open(
        os.path.join(os.path.dirname("__file__"), "README.md"), encoding="utf-8"
    ).read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/Alpaca00/pytest-schedule",
    download_url="https://github.com/Alpaca00/pytest-schedule",
    keywords=[
        "schedule",
        "periodic",
        "jobs",
        "scheduling",
        "clockwork",
        "cron",
        "scheduler",
        "job scheduling",
        "test job scheduling",
        "pytest job scheduling",
        "unittest job scheduling",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_reqs=parse_requirements('requirements-dev.txt', session='hack'),
    entry_points={
            "console_scripts": [
                "pytest-schedule = pytest_schedule",
            ]
        },
)
