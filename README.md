#### pytest-schedule

The job of test scheduling for humans.

#### Installation

```
pip install pytest-schedule
```
You should to install the Pytest library if it's not already installed
```
pip install pytest
```

##### Usage:

#### Generate a tree of test module names, recursively, for the root directory of **pytest_schedule.json**
```
python -m pytest_schedule.generate schedule_json
```

##### Run tests with any custom tags from **pytest_schedule.json**

```
python -m pytest_schedule -t tag

python -m pytest_schedule --tags smoke,unittest,integration

python -m pytest_schedule --tag unittest --test_module unittest

python -m pytest_schedule --tag unittest --test_module pytest

```

##### Change the time to 00:00:00 according to the template in the pytest_schedule.json file
```
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
```

#### The following options are available by the command:
```
$ python -m pytest_schedule --help
```