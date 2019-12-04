import os
import pytest

from validator.utils import FileTypeException
from validator.validator import validate_file


@pytest.fixture(scope='session')
def xls_file():
    path = os.path.dirname(os.path.realpath(__file__))
    xls_file_path = os.path.join(path, 'data', 'test-brownfield-register.xls')
    yield xls_file_path
    test_output_file = os.path.join(path, 'data', 'test-brownfield-register.xls.csv')
    os.remove(test_output_file)


@pytest.fixture(scope='session')
def xlsx_file():
    path = os.path.dirname(os.path.realpath(__file__))
    xlsx_file_path = os.path.join(path, 'data', 'test-brownfield-register.xlsx')
    yield xlsx_file_path
    test_output_file = os.path.join(path, 'data', 'test-brownfield-register.xlsx.csv')
    os.remove(test_output_file)


@pytest.fixture(scope='session')
def xlsm_file():
    path = os.path.dirname(os.path.realpath(__file__))
    xlsm_file_path = os.path.join(path, 'data', 'test-brownfield-register.xlsm')
    yield xlsm_file_path
    test_output_file = os.path.join(path, 'data', 'test-brownfield-register.xlsm.csv')
    os.remove(test_output_file)


@pytest.fixture(scope='session')
def not_a_csv_file():
    path = os.path.dirname(os.path.realpath(__file__))
    not_a_csv_file_path = os.path.join(path, 'data', 'this_is_not_a_csv.pdf')
    yield not_a_csv_file_path
    test_output_file = f'{not_a_csv_file_path}.csv'
    os.remove(test_output_file)


def test_can_handle_xls_file(xls_file, schema_file):

    result = validate_file(xls_file, schema_file)

    assert result.result['tables'][0]['error-count'] == 10
    assert len(result.input) == 2
    assert result.meta_data['file_type'] == 'xls'


def test_can_handle_xlsx_file(xlsx_file, schema_file):

    result = validate_file(xlsx_file, schema_file)

    assert result.result['tables'][0]['error-count'] == 10
    assert len(result.input) == 2
    assert result.meta_data['file_type'] == 'xls'


# Note in this test there are additional date errors because of how xls2csv interprets dates.
# A date format can be passed as flag to that call but we can't be sure what date formats
# to expect as input
def test_xlsm_file(xlsm_file, schema_file):

    result = validate_file(xlsm_file, schema_file)

    assert result.result['tables'][0]['error-count'] == 14
    assert len(result.input) == 2
    assert result.meta_data['file_type'] == 'xlsm'


def test_file_that_cannot_be_converted_to_csv_throws_exception(not_a_csv_file, schema_file):

    with pytest.raises(FileTypeException):
        validate_file(not_a_csv_file, schema_file)
