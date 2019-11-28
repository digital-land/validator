import sys

import click

from validator.presenter.console import ConsoleResultPresenter
from validator.presenter.html import HtmlResultPresenter
from validator.presenter.json import JsonResultPresenter
from validator.utils import BrownfieldStandard
from validator.validator import validate_file

brownfield_v2_schema = BrownfieldStandard.v2_standard_schema()

schema_help_text = "The path to the schema.json to validate file against. The default is version 2 of the Brownfield land data standard contained in this package."  # noqa
output_format_help_text = '''The output format of the result. The default, 'console' prints a summary result to the console.
                             The options 'html' or 'json' will output the result as html or json to the console, so redirect the output create an html or json file.'''  # noqa


@click.command()
@click.option("--file", help="The path to the CSV file to validate.", required=True)
@click.option("--schema", help=schema_help_text, default=brownfield_v2_schema)
@click.option("--output", type=click.Choice(['console', 'html', 'json']), help=output_format_help_text, default='console')  # noqa
def validate(file, schema, output):
    try:
        result = validate_file(file, schema)
        if output == 'console':
            out = ConsoleResultPresenter(result)
        elif output == 'html':
            out = HtmlResultPresenter(result)
        elif output == 'json':
            out = JsonResultPresenter(result)
        print(out)
        sys.exit(0)
    except Exception as e:
        sys.exit(-1)


if __name__ == '__main__':
    validate()
