#### pytest-schedule

**Automate and customize test scheduling effortlessly on local machines.**

### Installation

To install pytest-schedule, use the following command:

```bash
pip install pytest-schedule
```

Make sure you have pytest installed as well:

```bash
pip install pytest
```

<hr>

### Usage

#### Generate a Test Tree

To recursively generate a JSON tree of test module names from the root directory, use:

```bash
python -m pytest_schedule.generate schedule_json
```

This will create a file named `schedule.json` in the root directory.

<hr>

#### Run Tests with Custom Tags

Execute tests with specific tags as defined in `pytest_schedule.json`.

#### Examples:

```bash
python -m pytest_schedule -t <tag>
python -m pytest_schedule --tags smoke,unittest,integration
python -m pytest_schedule --tag unittest --test_module unittest
python -m pytest_schedule --tag unittest --test_module pytest
```

#### Schedule Test Execution Times

To set specific test execution times, modify pytest_schedule.json following this structure:

```json
{
  "0.0.7": [
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
          "test_module_binary_tree_2_0_0.py": "00:00:00"
        }
      ]
    }
  ]
}
```

<hr>

#### Command Options

To see all available options, run:

```bash
python -m pytest_schedule --help
```

<hr>

### Logging

Stdout logs are generated in the following format:

```text
[10:49:35] | PYTEST-SCHEDULE |  The job process started.
[10:49:35] | PYTEST-SCHEDULE |   (1) tag::test_a.py::11:50:00 task waiting ..
[10:50:00] | PYTEST-SCHEDULE |   (1) tag::test_a.py::11:50:00 task started ..
[10:50:00] | PYTEST-SCHEDULE |   (1) tag::test_a.py::11:50:00 task completed   [FAILED]
[10:50:00] | PYTEST-SCHEDULE |  The job process finished.
```

The log file is generated in the root directory with the name `pytest_schedule.log`.
