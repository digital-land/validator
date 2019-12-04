import sys

import click

from validator.presenter.json import JsonResultPresenter
from validator.utils import BrownfieldStandard
from validator.validator import validate_file

brownfield_v2_schema = BrownfieldStandard.v2_standard_schema()

schema_help_text = "The path to the schema.json to validate file against. The default is version 2 of the Brownfield land data standard contained in this package."  # noqa


@click.command()
@click.option("--file", help="The path to the CSV file to validate.", required=True)
@click.option("--schema", help=schema_help_text, default=brownfield_v2_schema)
def validate(file, schema):
    try:
        result = validate_file(file, schema)
        out = JsonResultPresenter(result)
        print(out)
        sys.exit(0)
    except Exception as e:
        sys.exit(-1)


if __name__ == '__main__':
    validate()
