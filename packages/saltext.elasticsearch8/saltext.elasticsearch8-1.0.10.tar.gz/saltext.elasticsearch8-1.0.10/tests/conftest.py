import os

import pytest
from saltext.elasticsearch8 import PACKAGE_ROOT
from saltfactories.utils import random_string


@pytest.fixture(scope="session")
def salt_factories_config():
    """
    Return a dictionary with the keyworkd arguments for FactoriesManager
    """
    return {
        "code_dir": str(PACKAGE_ROOT),
        "inject_coverage": "COVERAGE_PROCESS_START" in os.environ,
        "inject_sitecustomize": "COVERAGE_PROCESS_START" in os.environ,
        "start_timeout": 120 if os.environ.get("CI") else 60,
    }


@pytest.fixture(scope="package")
def master(salt_factories):
    return salt_factories.get_salt_master_daemon(random_string("master-"))


@pytest.fixture(scope="package")
def minion(master):
    return master.get_salt_minion_daemon(random_string("minion-"))
