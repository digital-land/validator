import logging
import goodtables

from validator.utils import extract_data, FileTypeException, logging_handler
from validator.validation_result import Result


custom_checks = ['geox-check', 'geoy-check', 'url-list-check']  # TODO the list of checks could be config or cli options?
builtin_checks = ['structure', 'schema']
checks = builtin_checks + custom_checks

logger = logging.getLogger(__name__)
logger.addHandler(logging_handler)


def validate_file(file, schema):
    try:
        extracted = extract_data(file)

        data = extracted.get('data')
        rows = extracted.get('rows')
        meta_data = extracted.get('meta_data')

        result = check_data(rows, schema)

        return Result(result=result,
                      upload=data,
                      rows=rows,
                      meta_data=meta_data)

    except FileTypeException as e:
        logger.exception(e)
        raise e


def check_data(data, schema):
    return goodtables.validate(data, schema=schema, order_fields=True, checks=checks)


# TODO - I don't think this is really needed here, it can be moved to the
# brownfield validator web app as it's more relevant in that context
def revalidate_result(result, schema):
    res = check_data(result.rows, schema)
    return Result(id=result.id,
                  result=res,
                  upload=result.upload,
                  rows=result.rows,
                  meta_data=result.meta_data)
