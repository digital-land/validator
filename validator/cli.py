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
@click.option("--output", help="Path of the output.", required=False)
@click.option(
    "--schema",
    default="brownfield",
    help="Path of the schema.json to validate file against."
    "The default is the 2019 Brownfield land data standard contained in this package.",
)
@click.option(
    "--csv-dir", help="Path of the directory to create intermediate CSV files."
)
@click.option(
    "--include-input/--exclude-input",
    " /-I",
    default=True,
    help="Exclude a copy of the input in the results.",
)
@click.option(
    "--include-rows/--exclude-rows",
    " /-R",
    default=True,
    help="Exclude harmonised rows in results.",
)
def validate(file, schema, csv_dir, include_input, include_rows, output):
    if csv_dir:
        validator.utils.csv_dir = csv_dir

    try:
        if schema == "brownfield":
            standard = BrownfieldStandard()
        else:
            standard = Standard(schema)

        result = validate_file(file, standard)
        result = result.to_dict(include_input=include_input, include_rows=include_rows)

        out = json.dumps(result)
        if output:
            with open(output, "w") as f:
                print(out, file=f)
        else:
            print(out)
        sys.exit(0)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    validate()
