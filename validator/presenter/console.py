
class ConsoleResultPresenter:

    def __init__(self, result):
        self.result = result

    def __str__(self):
        headers = '\n\t'.join(self.result.headers_found())
        missing = '\n\t'.join(self.result.missing_headers())
        additional = '\n\t'.join(self.result.additional_headers())

        return f'''
        Validation result
        =================
        File valid: {self.result.valid()}
        Row count: {self.result.row_count()}
        Valid row count: {self.result.valid_row_count()}

        Headers found
        =============
        {headers}

        Missing headers
        =============
        {missing}

        Additional headers
        =============
        {additional}
        '''
