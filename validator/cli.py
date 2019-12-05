import sys
import click

from validator.presenter.json import JsonResultPresenter
from validator.standards import BrownfieldStandard, Standard
from validator.validator import validate_file


schema_help_text = "The path to the schema.json to validate file against. The default is version 2 of the Brownfield land data standard contained in this package."  # noqa


@click.command()
@click.option("--file", help="The path to the CSV file to validate.", required=True)
@click.option("--schema", help=schema_help_text, default='brownfield')
def validate(file, schema):
    try:
        if schema == 'brownfield':
            standard = BrownfieldStandard()
        else:
            standard = Standard(schema)

        result = validate_file(file, standard)

        out = JsonResultPresenter(result)
        print(out)
        sys.exit(0)
    except Exception as e:
        sys.exit(-1)


if __name__ == '__main__':
    validate()
