from bidict import bidict

from validator.error_mapper import ErrorMapper


class Result:

    def __init__(self,
                 result,
                 input,
                 rows,
                 meta_data,
                 standard,
                 errors_by_row=None,
                 errors_by_column=None,
                 id=None):

        self.id = id
        self.result = result
        self.input = input
        self.rows = rows
        self.meta_data = meta_data
        self.standard = standard

        # The following methods set state on this object so attributes above all need to be
        # set before this point

        self.result['tables'][0].setdefault('headers', {})

        cols_to_headers = {}
        for column_number, header in enumerate(self.result['tables'][0]['headers']):
            cols_to_headers[column_number + 1] = header
        self.column_numbers_to_headers = bidict(cols_to_headers)

        if errors_by_row is None:
            self.errors_by_row = self.collect_row_errors()
        else:
            self.errors_by_row = errors_by_row
        if errors_by_column is None:
            self.errors_by_column = self.collect_column_errors()
        else:
            self.errors_by_column = errors_by_column

    @staticmethod
    def factory(result_dict, standard):
        result = Result(result=result_dict['result'],
                        input=result_dict.get('input'),
                        rows=result_dict.get('rows'),
                        meta_data=result_dict['meta_data'],
                        errors_by_row=result_dict['errors_by_row'],
                        errors_by_column=result_dict['errors_by_column'],
                        standard=standard)
        return result

    def valid(self):
        return self.result['valid']

    def row_count(self):
        return self.result['tables'][0]['row-count']

    def headers_found(self):
        return self.meta_data['headers_found']

    def correct_headers_found(self):
        return list(set(self.headers_found()) - set(self.additional_headers()))

    def extra_headers_found(self):
        return list(set(self.additional_headers()) - set(self.standard.headers_deprecated()))

    def deprecated_headers_found(self):
        return list(set(self.additional_headers()) - set(self.extra_headers_found()))

    def additional_headers(self):
        return self.meta_data.get('additional_headers')

    def missing_headers(self):
        return self.meta_data.get('missing_headers')

    def reconcile_header_results(self, headers_added, headers_removed):
        additional_headers = self.additional_headers()
        additional_headers = set(additional_headers) - set(headers_added)
        additional_headers = set(additional_headers) - set(headers_removed)
        self.meta_data['additional_headers'] = list(additional_headers)

        missing_headers = self.missing_headers()
        missing_headers = set(missing_headers) - set(headers_added)
        self.meta_data['missing_headers'] = list(missing_headers)

        headers_found = self.headers_found()
        headers_found = set(headers_found) - set(headers_removed)
        headers_found.update(headers_added)
        self.meta_data['headers_found'] = list(headers_found)

    def media_type(self):
        return self.meta_data.get('media_type')

    def suffix(self):
        return self.meta_data.get('suffix')

    def error_count(self):
        return self.result.get('error-count')

    def check_headers(self):
        report_headers = self.headers_found()
        headers_status = "Headers correct"
        for header in self.standard.current_standard_headers():
            if header not in report_headers:
                headers_status = "Missing headers"
        for header in self.standard.headers_deprecated():
            if header in report_headers:
                headers_status = "Warnings"
        if len(self.additional_headers()) > 0:
            headers_status = "Extra headers"
        return headers_status

    def column_number_to_header(self, index):
        try:
            return self.column_numbers_to_headers[index]
        except KeyError as e: # noqa
            return 'unknown'

    def header_to_column_number(self, header):
        try:
            return self.column_numbers_to_headers.inverse[header]
        except KeyError as e: # noqa
            return -1

    def collect_column_errors(self):
        errs = {}
        for column in self.standard.current_standard_headers():
            errs = {**errs, **self.collect_errors_by_column(column)}
        return errs

    def collect_errors_by_column(self, column):
        column_number = self.header_to_column_number(column)
        messages = set([])
        errs = []
        rows = []
        errors = {}
        for e in self.result['tables'][0]['errors']:
            mapper = ErrorMapper.factory(e, column)
            if e.get('column-number') is not None and e.get('column-number') == column_number:
                if 'row-number' in e.keys():
                    rows.append(e['row-number'])
                messages.add(mapper.overall_error_messages())
                value = e.get('message-data').get('value') if e.get('message-data') else None
                err = {'message': mapper.field_error_message(),
                       'row': e.get('row-number', 0),
                       'fix': mapper.get_fix_if_possible(),
                       'value': value
                       }
                errs.append(err)
        if errs:
            errors[column] = {'rows': rows,
                              'errors': errs,
                              'messages': list(messages)}
        return errors

    def collect_row_errors(self):
        rows = []
        for row_number, data_row in enumerate(self.rows):
            row = {}
            for header, value in data_row.items():
                error = self.collect_errors_by_row(header, row_number + 1)
                row[header] = {'value': value, 'error': error, 'row': row_number + 1}
            rows.append(row)
        return rows

    def collect_errors_by_row(self, header, row_number):
        error = None
        column_number = self.header_to_column_number(header)
        for e in self.result['tables'][0]['errors']:
            mapper = ErrorMapper.factory(e, header)
            if e.get('column-number') is not None and e.get('column-number') == column_number \
                    and e.get('row-number') == row_number:
                error = {'message': mapper.field_error_message(), 'fix': mapper.get_fix_if_possible()}
        return error

    def valid_row_count(self):
        return self.row_count() - len(self.invalid_rows())

    def invalid_rows(self):
        rows = []
        for error in self.result['tables'][0]['errors']:
            if 'row-number' in error.keys():
                rows.append(error['row-number'])
        return set(rows)

    def apply_fixes(self, column):
        fixes_applied = []
        column_errors = self.errors_by_column.get(column)
        if column_errors is not None and column_errors.get('errors') is not None:
            for error in column_errors.get('errors'):
                row = error['row'] - 1  # row numbers are not zero indexed
                fix = error['fix']
                value = error['value']
                if self.rows[row][column] == value and fix is not None:
                    self.rows[row][column] = fix
                    fixes_applied.append({'row': error['row'], 'from': value, 'to': fix})
        return fixes_applied

    def to_dict(self, include_input=False, include_rows=False):
        result = {
            'id': str(self.id) if self.id else None,
            'meta_data': {
                'headers_expected': self.standard.current_standard_headers(),
                'headers_deprecated': self.standard.headers_deprecated(),
                'headers_found': self.headers_found(),
                'missing_headers': self.missing_headers(),
                'additional_headers': self.additional_headers(),
                'media_type': self.media_type(),
                'suffix': self.suffix(),
                'invalid_row_count': len(self.invalid_rows()),
            },
            'errors_by_row': self.errors_by_row,
            'errors_by_column': self.errors_by_column,
            'result': self.result
        }

        if include_input:
            result['input'] = self.input

        if include_rows:
            result['rows'] = self.rows

        return result
