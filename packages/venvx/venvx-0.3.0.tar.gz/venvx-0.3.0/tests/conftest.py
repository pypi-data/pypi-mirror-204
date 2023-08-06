
import pytest


# region Add a cmd line switch --slow

# Test cases decorated with
# @pytest.mark.slow
# will not be run unless pytest is invoked with the --slow command line switch.

def pytest_addoption(parser):
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )

def pytest_configure(config):
    config.addinivalue_line("markers",
                            "slow: mark a test as slow to run")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--slow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="use --slow option to run this")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)

# endregion
