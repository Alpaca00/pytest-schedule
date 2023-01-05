#### pytest-schedule

The job of test scheduling for humans.


##### Usage:

#### Generate a tree of test module names, recursively, for the root directory of **pytest_schedule.json**
```
python -m pytest_schedule.generate schedule_json
```

##### Run tests with any custom tags from **pytest_schedule.json**

```
python -m pytest_schedule -t tag

python -m pytest_schedule --tags unittest,api,integration

python -m pytest_schedule --tag unittest --test_module unittest

python -m pytest_schedule --tag unittest --test_module pytest

```

#### The following options are available by the command:
```
$ python -m pytest_schedule --help
```