from decimal import Decimal
from tableschema import Field
from validator import geox_check, geoy_check

from validator.checks import MAXIMUM_UK_LONGITUDE
from validator.checks import MINIMUM_UK_LONGITUDE
from validator.checks import MAXIMUM_UK_LATITUDE
from validator.checks import MINIMUM_UK_LATITUDE


def test_geox_looks_like_correct_coordinate_reference_system():

    field = {'name': 'GeoX',
             'title': 'GeoX',
             'description': 'Does not matter for this test',
             'type': 'number',
             'constraints': {'required': True},
             'format': 'default'}

    field = Field(field, missing_values=[])

    cells = [{'header': 'GeoX',
            'field': field,
            'value': Decimal('139531'),
            'column-number': 4,
            'number': 4,
            'row-number': 1}]

    errors = geox_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '139531 isn\'t a longitude using the WGS84 or ETRS89 coordinate systems'


def test_geox_not_more_than_6_decimal_places():

    field = {'name': 'GeoX',
             'title': 'GeoX',
             'description': 'Does not matter for this test',
             'type': 'number',
             'constraints': {'required': True},
             'format': 'default'}

    field = Field(field, missing_values=[])

    cells = [{'header': 'GeoX',
            'field': field,
            'value': Decimal('-1.1234567'),
            'column-number': 4,
            'number': 4,
            'row-number': 1}]

    errors = geox_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '-1.1234567 should not have more than six decimal places'


def test_geox_should_be_within_bounds_of_uk_longitude():

    field = {'name': 'GeoX',
             'title': 'GeoX',
             'description': 'Does not matter for this test',
             'type': 'number',
             'constraints': {'required': True},
             'format': 'default'}

    field = Field(field, missing_values=[])

    cells = [{'header': 'GeoX',
              'field': field,
              'value': Decimal(f'{MINIMUM_UK_LONGITUDE - 1}'),
              'column-number': 4,
              'number': 4,
              'row-number': 1}]

    errors = geox_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '-8 is not a longitude within the UK'

    cells = [{'header': 'GeoX',
              'field': field,
              'value': Decimal(f'{MAXIMUM_UK_LONGITUDE + 1}'),
              'column-number': 4,
              'number': 4,
              'row-number': 1}]

    errors = geox_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '3 is not a longitude within the UK'



def test_geoy_looks_like_correct_coordinate_reference_system():

    field = {'name': 'GeoY',
             'title': 'GeoY',
             'description': 'Does not matter for this test',
             'type': 'number',
             'constraints': {'required': True},
             'format': 'default'}

    field = Field(field, missing_values=[])

    cells = [{'header': 'GeoY',
            'field': field,
            'value': Decimal('543216'),
            'column-number': 4,
            'number': 4,
            'row-number': 1}]

    errors = geoy_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '543216 isn\'t a latitude using the WGS84 or ETRS89 coordinate systems'


def test_geoy_not_more_than_6_decimal_places():

    field = {'name': 'GeoY',
             'title': 'GeoY',
             'description': 'Does not matter for this test',
             'type': 'number',
             'constraints': {'required': True},
             'format': 'default'}

    field = Field(field, missing_values=[])

    cells = [{'header': 'GeoY',
            'field': field,
            'value': Decimal('50.1234567'),
            'column-number': 4,
            'number': 4,
            'row-number': 1}]

    errors = geoy_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '50.1234567 should not have more than six decimal places'


def test_geoy_should_be_within_bounds_of_uk_latitude():

    field = {'name': 'GeoY',
             'title': 'GeoY',
             'description': 'Does not matter for this test',
             'type': 'number',
             'constraints': {'required': True},
             'format': 'default'}

    field = Field(field, missing_values=[])

    cells = [{'header': 'GeoY',
              'field': field,
              'value': Decimal(f'{MINIMUM_UK_LATITUDE - 1}'),
              'column-number': 4,
              'number': 4,
              'row-number': 1}]

    errors = geoy_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '48 is not a latitude within the UK'

    cells = [{'header': 'GeoY',
              'field': field,
              'value': Decimal(f'{MAXIMUM_UK_LATITUDE + 1}'),
              'column-number': 4,
              'number': 4,
              'row-number': 1}]

    errors = geoy_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'geo-error'
    assert errors[0].message == '58 is not a latitude within the UK'
