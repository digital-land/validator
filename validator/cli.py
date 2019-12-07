import sys
import click
import json

from validator.standards import BrownfieldStandard, Standard
from validator.validator import validate_file
from validator.logger import get_logger
import validator.utils


logger = get_logger(__name__)


@click.command()
@click.option("--file", help="Path of the file to validate.", required=True)
@click.option(
    "--schema",
    default="brownfield",
    help="Path of the schema.json to validate file against."
    "The default is the 2019 Brownfield land data standard contained in this package.",
)
@click.option(
    "--csvdir", help="Path of the directory to create intermediate CSV files."
)
@click.option(
    "--include-input/--exclude-input",
    " /-i",
    default=True,
    help="Exclude a copy of the input in the results.",
)
def validate(file, schema, csvdir, include_input):
    if csvdir:
        validator.utils.csvdir = csvdir

    try:
        if schema == "brownfield":
            standard = BrownfieldStandard()
        else:
            standard = Standard(schema)

        result = validate_file(file, standard)
        result = result.to_dict()

        if not include_input:
            del result['input']

        out = json.dumps(result)
        print(out)
        sys.exit(0)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    validate()
