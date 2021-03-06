import codecs
import collections
import sys
import csv
import os
from os.path import basename, dirname
import pandas as pd
import magic
import mimetypes

from cchardet import UniversalDetector
from validator.logger import get_logger

tmp_dir = None

logger = get_logger(__name__)


def extract_data(path, standard):
    if looks_like_csv(path):
        media_type = 'text/csv'
    else:
        path, media_type = convert_to_csv(path)

    return csv_to_dict(path, media_type, standard)


def convert_to_csv(path):
    media_type = magic.from_file(path, mime=True)
    tmp_path = csv_path(tmp_dir, path)

    try:
        excel = pd.read_excel(path)
    except:
        excel = None

    if excel is not None:
        excel.to_csv(tmp_path, index=None, header=True)
        return tmp_path, media_type

    logger.info(f"Unable to convert {path} from {media_type} to CSV")
    with open(tmp_path, 'w') as out:
        pass
    return tmp_path, media_type


def csv_to_dict(csv_file, media_type, standard):
    result = {
        'meta_data': {
                'headers_found': [],
                'additional_headers': [],
                'missing_headers': [],
                'media_type': media_type,
                'suffix': suffix_for_media_type(media_type),
        },
        'rows': [],
        'data': [],
    }

    encoding = detect_encoding(csv_file)
    with codecs.open(csv_file, encoding=encoding['encoding']) as f:
        reader = csv.DictReader(f)

        if reader.fieldnames:
            result['meta_data']['headers_found'] = reader.fieldnames

        result['meta_data']['additional_headers'] = list(set(result['meta_data']['headers_found']) - set(standard.current_standard_headers()))
        result['meta_data']['missing_headers'] = list(set(standard.current_standard_headers()) - set(result['meta_data']['headers_found']))

        for row in reader:
            to_check = collections.OrderedDict()

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


def suffix_for_media_type(media_type):
    suffix = {
        'application/vnd.ms-excel': '.xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    }
    return suffix.get(media_type, mimetypes.guess_extension(media_type))


def get_markdown_for_field(field_name):
    from pathlib import Path
    current_directory = Path(__file__).parent.resolve()
    markdown_file = Path(current_directory, 'markdown', f'{field_name}.md')
    with open(markdown_file) as f:
        content = f.read()
    return content


def looks_like_csv(file):
    try:
        encoding = detect_encoding(file)
        with open(file, encoding=encoding['encoding']) as f:
            content = f.read()
            if content.lower().startswith('<!doctype html'):
                return False
            csv.Sniffer().sniff(content)
            return True
    except Exception as e:  # noqa
        return False


def csv_path(_dir, path):
    path = os.path.join(_dir, basename(path)) if _dir else path
    return path + ".csv"


def save_csv(data, file):
    if data:
        fieldnames = data[0].keys()
        if fieldnames:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
