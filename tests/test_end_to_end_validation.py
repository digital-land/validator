from validator.validator import validate_file


def test_check_uploaded_data_in_end_to_end_validation(csv_file, schema_file, upload):

    result = validate_file(csv_file, schema_file)

    assert result.result['tables'][0]['error-count'] == 8
    assert len(result.upload) == 2
    assert len(result.upload) == len(upload)
    assert set(result.upload[0].keys()) == set(upload[0].keys())
    assert set(result.upload[1].keys()) == set(upload[1].keys())
    assert set(result.upload[0].values()) == set(upload[0].values())
    assert set(result.upload[1].values()) == set(upload[1].values())


def test_check_extracted_rows_in_end_to_end_validation(csv_file, schema_file, rows):

    result = validate_file(csv_file, schema_file)

    assert result.result['tables'][0]['error-count'] == 8
    assert len(result.rows) == 2
    assert len(result.rows) == len(rows)
    assert set(result.rows[0].keys()) == set(rows[0].keys())
    assert set(result.rows[1].keys()) == set(rows[1].keys())
    assert set(result.rows[0].values()) == set(rows[0].values())
    assert set(result.rows[1].values()) == set(rows[1].values())


def test_check_errors_by_column_in_end_to_end_validation(csv_file, schema_file):

    result = validate_file(csv_file, schema_file)

    assert len(result.errors_by_column['GeoX']['errors']) == 2
    assert len(result.errors_by_column['GeoY']['errors']) == 2
    assert len(result.errors_by_column['SiteplanURL']['errors']) == 1
    assert len(result.errors_by_column['PlanningHistory']['errors']) == 1

    assert result.errors_by_column['GeoX']['rows'] == [1, 2]
    assert result.errors_by_column['GeoY']['rows'] == [1, 2]
    assert result.errors_by_column['SiteplanURL']['rows'] == [1]
    assert result.errors_by_column['PlanningHistory']['rows'] == [1]


def test_check_errors_by_row_in_end_to_end_validation(csv_file, schema_file):

    result = validate_file(csv_file, schema_file)

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
