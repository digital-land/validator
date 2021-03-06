from validator.validator import validate_file


def test_check_uploaded_data_in_end_to_end_validation(csv_file, standard, input):

    result = validate_file(csv_file, standard)

    assert result.result['tables'][0]['error-count'] == 10
    assert len(result.input) == 2
    assert len(result.input) == len(input)
    assert set(result.input[0].keys()) == set(input[0].keys())
    assert set(result.input[1].keys()) == set(input[1].keys())
    assert set(result.input[0].values()) == set(input[0].values())
    assert set(result.input[1].values()) == set(input[1].values())


def test_check_extracted_rows_in_end_to_end_validation(csv_file, standard, rows):

    result = validate_file(csv_file, standard)

    assert result.result['tables'][0]['error-count'] == 10
    assert len(result.rows) == 2
    assert len(result.rows) == len(rows)
    assert set(result.rows[0].keys()) == set(rows[0].keys())
    assert set(result.rows[1].keys()) == set(rows[1].keys())
    assert set(result.rows[0].values()) == set(rows[0].values())
    assert set(result.rows[1].values()) == set(rows[1].values())


def test_check_errors_by_column_in_end_to_end_validation(csv_file, standard):

    result = validate_file(csv_file, standard)

    assert len(result.errors_by_column['GeoX']['errors']) == 2
    assert len(result.errors_by_column['GeoY']['errors']) == 2
    assert len(result.errors_by_column['SiteplanURL']['errors']) == 1
    assert len(result.errors_by_column['PlanningHistory']['errors']) == 1

    assert result.errors_by_column['GeoX']['rows'] == [1, 2]
    assert result.errors_by_column['GeoY']['rows'] == [1, 2]
    assert result.errors_by_column['SiteplanURL']['rows'] == [1]
    assert result.errors_by_column['PlanningHistory']['rows'] == [1]


def test_check_errors_by_row_in_end_to_end_validation(csv_file, standard):

    result = validate_file(csv_file, standard)

    assert len(result.errors_by_row) == 2

    assert result.errors_by_row[0]['GeoX']['row'] == 1
    assert result.errors_by_row[0]['GeoX']['error'] is not None

    assert result.errors_by_row[1]['GeoX']['row'] == 2
    assert result.errors_by_row[1]['GeoX']['error'] is not None

    assert result.errors_by_row[0]['GeoY']['row'] == 1
    assert result.errors_by_row[0]['GeoY']['error'] is not None

    assert result.errors_by_row[1]['GeoY']['row'] == 2
    assert result.errors_by_row[1]['GeoY']['error'] is not None

    assert result.errors_by_row[0]['SiteplanURL']['row'] == 1
    assert result.errors_by_row[0]['SiteplanURL']['error'] is not None

    assert result.errors_by_row[1]['SiteplanURL']['row'] == 2
    assert result.errors_by_row[1]['SiteplanURL']['error'] is None

    assert result.errors_by_row[0]['PlanningHistory']['row'] == 1
    assert result.errors_by_row[0]['PlanningHistory']['error'] is not None

    assert result.errors_by_row[1]['PlanningHistory']['row'] == 2
    assert result.errors_by_row[1]['PlanningHistory']['error'] is None
