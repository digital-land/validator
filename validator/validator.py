import logging
import goodtables

from validator.utils import extract_data
from validator.validation_result import Result
from validator.logger import get_logger

logger = get_logger(__name__)


def validate_file(file, standard):
    extracted = extract_data(file, standard)
    data = extracted.get('data')
    rows = extracted.get('rows')
    meta_data = extracted.get('meta_data')

    result = check_data(rows, standard.schema)

    return Result(result=result,
                  input=data,
                  rows=rows,
                  meta_data=meta_data,
                  standard=standard)


def check_data(data, schema):
    custom_checks = ['geox-check', 'geoy-check', 'url-list-check']  # TODO the list of checks could be config or cli options?
    builtin_checks = ['structure', 'schema']
    checks = builtin_checks + custom_checks
    return goodtables.validate(data, schema=schema, order_fields=True, checks=checks)
