import os
import pytest

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
def pdf_file():
    path = os.path.dirname(os.path.realpath(__file__))
    pdf_file = os.path.join(path, 'data', 'this_is_not_a_csv.pdf')
    yield pdf_file
    test_output_file = f'{pdf_file}.csv'
    os.remove(test_output_file)


def test_can_handle_xls_file(xls_file, standard):

    result = validate_file(xls_file, standard)

    assert result.result['tables'][0]['error-count'] == 8
    assert len(result.input) == 2
    assert result.meta_data['media_type'] == 'application/vnd.ms-excel'
    assert result.meta_data['suffix'] == '.xls'


def test_can_handle_xlsx_file(xlsx_file, standard):

    result = validate_file(xlsx_file, standard)

    assert result.result['tables'][0]['error-count'] == 8
    assert len(result.input) == 2
    assert result.meta_data['media_type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert result.meta_data['suffix'] == '.xlsx'


# Note in this test there are additional date errors because of how xls2csv interprets dates.
# A date format can be passed as flag to that call but we can't be sure what date formats
# to expect as input
def test_xlsm_file(xlsm_file, standard):

    result = validate_file(xlsm_file, standard)

    assert result.result['tables'][0]['error-count'] == 8
    assert len(result.input) == 2
    assert result.meta_data['media_type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert result.meta_data['suffix'] == '.xlsx'


def test_can_handle_pdf_file(pdf_file, standard):

    result = validate_file(pdf_file, standard)
    assert result.meta_data['media_type'] == 'application/pdf'
    assert result.meta_data['suffix'] == '.pdf'
