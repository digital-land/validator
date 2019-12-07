import codecs
import collections
import sys
import csv
from os.path import basename, dirname

import subprocess
from cchardet import UniversalDetector
from validator.logger import get_logger

csvdir = None

logger = get_logger(__name__)


def try_convert_to_csv(path):

    csvfile = csvdir + basename(path) if csvdir else path
    csvfile = csvfile + ".csv"

    try:
        with open(csvfile, 'w') as out:
            subprocess.check_call(['in2csv', path], stdout=out)
        return csvfile, 'xls'
    except subprocess.CalledProcessError as e:
        logger.info("in2csv failed: " + str(e))

    try:
        with open(csvfile, 'w') as out:
            subprocess.check_call(['xlsx2csv', path], stdout=out)
        return csvfile, 'xlsm'
    except subprocess.CalledProcessError as e:
        logger.info("xlsx2csv failed: " + str(e))

    logger.info(f"Unable to convert {path} to CSV")
    with open(csvfile, 'w') as out:
        return csvfile, 'unknown'


def extract_data(file, standard):
    original_file_type = 'csv'
    if not _looks_like_csv(file):
        file, original_file_type = try_convert_to_csv(file)
    return csv_to_dict(file, original_file_type, standard)


def csv_to_dict(csv_file, original_file_type, standard):
    result = {
        'meta_data': {
                'headers_found': [],
                'additional_headers': [],
                'missing_headers': [],
                'planning_authority': "Unknown",
                'file_type': original_file_type
        },
        'rows': [],
        'data': [],
    }

    encoding = detect_encoding(csv_file)
    planning_authority = None
    with codecs.open(csv_file, encoding=encoding['encoding']) as f:
        reader = csv.DictReader(f)

        if reader.fieldnames:
            result['meta_data']['headers_found'] = reader.fieldnames

        result['meta_data']['additional_headers'] = list(set(result['meta_data']['headers_found']) - set(standard.current_standard_headers()))
        result['meta_data']['missing_headers'] = list(set(standard.current_standard_headers()) - set(result['meta_data']['headers_found']))

        for row in reader:
            to_check = collections.OrderedDict()

            # TODO replace planning authority with "organisation"
            result['meta_data']['planning_authority'] = row.get('OrganisationLabel', 'Unknown')

            for column in standard.current_standard_headers():
                value = row.get(column, None)
                if value is not None:
                    to_check[column] = row.get(column)

            result['rows'].append(to_check)
            result['data'].append(row)

    return result


def detect_encoding(file):
    detector = UniversalDetector()
    detector.reset()
    with open(file, 'rb') as f:
        for row in f:
            detector.feed(row)
            if detector.done:
                break
    detector.close()
    return detector.result


def get_markdown_for_field(field_name):
    from pathlib import Path
    current_directory = Path(__file__).parent.resolve()
    markdown_file = Path(current_directory, 'markdown', f'{field_name}.md')
    with open(markdown_file) as f:
        content = f.read()
    return content


def _looks_like_csv(file):
    try:
        encoding = detect_encoding(file)
        with open(file, encoding=encoding['encoding']) as f:
            content = f.read()
            csv.Sniffer().sniff(content)
            return True
    except Exception as e:  # noqa
        return False
