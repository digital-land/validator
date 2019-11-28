# flake8: noqa

from validator import url_list_check


def test_url_list_check_fails_if_contains_a_value_that_is_not_a_url():

    field = {'name': 'PlanningHistory',
             'title': 'Planning history',
             'description': 'Links to any web pages that give information on the site’s planning history. Multiple links must be separated by pipe character',
             'type': 'string',
             'constraints': {'required': False}
             }

    cell = {'header': 'PlanningHistory',
            'field': field,
            'value': 'https://www.winchester.gov.uk|this-item-is-not-a-url',
            'column-number': 15,
            'number': 15,
            'row-number': 1}

    cells = [cell]

    errors = url_list_check(cells)

    assert len(errors) == 1
    assert errors[0].code == 'url-list-error'
    assert errors[0].message == "'this-item-is-not-a-url' is not a url"


def test_url_list_check_passes_if_all_values_urls():

    field = {'name': 'PlanningHistory',
             'title': 'Planning history',
             'description': 'Links to any web pages that give information on the site’s planning history. Multiple links must be separated by pipe character',
             'type': 'string',
             'constraints': {'required': False}
             }

    cell = {'header': 'PlanningHistory',
            'field': field,
            'value': 'https://www.winchester.gov.uk|https://www.another-place.gov.uk',
            'column-number': 15,
            'number': 15,
            'row-number': 1}

    cells = [cell]

    errors = url_list_check(cells)

    assert len(errors) == 0