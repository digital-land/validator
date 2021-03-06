import os
import sys
import click
import canonicaljson

from validator.standards import BrownfieldStandard, Standard
from validator.validator import validate_file
from validator.logger import get_logger
import validator.utils


logger = get_logger(__name__)


@click.command()
@click.option("--file", help="Path of the input file to validate.", required=True)
@click.option(
    "--output", help="Path of the output file containing results.", required=False
)
@click.option(
    "--schema",
    default="brownfield",
    help="Path of the schema.json to validate file against."
    "The default is the 2019 Brownfield land data standard contained in this package.",
)
@click.option("--tmp-dir", help="Path of the directory to create converted CSV files.")
@click.option("--save-dir", help="Path of the directory to save a normalised CSV file.")
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
def validate(file, schema, tmp_dir, save_dir, include_input, include_rows, output):
    validator.utils.tmp_dir = tmp_dir

    try:
        if schema == "brownfield":
            standard = BrownfieldStandard()
        else:
            standard = Standard(schema)

        result = validate_file(file, standard)

        r = result.to_dict(include_input=include_input, include_rows=include_rows)
        out = canonicaljson.encode_canonical_json(r)
        if output:
            with open(output, "wb") as f:
                f.write(out)
        else:
            sys.stdout.buffer.write(out)

        if save_dir:
            save_path = validator.utils.csv_path(save_dir, file)
            with open(save_path, "w") as f:
                validator.utils.save_csv(result.input, file=f)

        sys.exit(0)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    validate()
