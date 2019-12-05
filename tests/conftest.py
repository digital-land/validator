import os
import pytest

from pathlib import Path
from validator.standards import BrownfieldStandard


@pytest.fixture(scope='session')
def input():
    from tests.data.test_data import input
    return input


@pytest.fixture(scope='session')
def rows():
    from tests.data.test_data import rows
    return rows


@pytest.fixture(scope='session')
def meta_data():
    from tests.data.test_data import meta_data
    return meta_data


@pytest.fixture(scope='session')
def csv_file():
    path = os.path.dirname(os.path.realpath(__file__))
    csv_file_path = os.path.join(path, 'data', 'test-brownfield-register.csv')
    return csv_file_path


@pytest.fixture(scope='session')
def standard():
    return BrownfieldStandard()
