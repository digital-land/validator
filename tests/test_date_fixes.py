from validator.validator import validate_file


def test_apply_date_fixes(csv_file, schema_file):
    result = validate_file(csv_file, schema_file)
    assert result.errors_by_column['LastUpdatedDate']['rows'] == [1,2]

    assert result.rows[0]['LastUpdatedDate'] == '8 Dec 2017'
    assert result.errors_by_column['LastUpdatedDate']['errors'][0]['value'] == '8 Dec 2017'
    assert result.errors_by_column['LastUpdatedDate']['errors'][0]['fix'] == '2017-12-08'

    assert result.rows[1]['LastUpdatedDate'] == '13/12/2017'
    assert result.errors_by_column['LastUpdatedDate']['errors'][1]['value'] == '13/12/2017'
    assert result.errors_by_column['LastUpdatedDate']['errors'][1]['fix'] == '2017-12-13'

    result.apply_fixes('LastUpdatedDate')

    assert result.rows[0]['LastUpdatedDate'] == '2017-12-08'
    assert result.rows[1]['LastUpdatedDate'] == '2017-12-13'