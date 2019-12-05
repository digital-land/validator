import json
import os


class Standard:

    def __init__(self, schema_path):
        with open(schema_path) as f:
           self.schema = json.load(f)

    def current_standard_headers(self):
        return [item['name'] for item in self.schema['fields']]

    def headers_deprecated(self):
        return []


class BrownfieldStandard(Standard):

    def __init__(self):
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema', 'brownfield-land-v2.json')
        super().__init__(schema_path)

    def headers_deprecated(self):
        previous_standard_headers = ['OrganisationURI',
                                     'OrganisationLabel',
                                     'SiteReference',
                                     'PreviouslyPartOf',
                                     'SiteNameAddress',
                                     'SiteplanURL',
                                     'CoordinateReferenceSystem',
                                     'GeoX',
                                     'GeoY',
                                     'Hectares',
                                     'OwnershipStatus',
                                     'Deliverable',
                                     'PlanningStatus',
                                     'PermissionType',
                                     'PermissionDate',
                                     'PlanningHistory',
                                     'ProposedForPIP',
                                     'MinNetDwellings',
                                     'DevelopmentDescription',
                                     'NonHousingDevelopment',
                                     'Part2',
                                     'NetDwellingsRangeFrom',
                                     'NetDwellingsRangeTo',
                                     'HazardousSubstances',
                                     'SiteInformation',
                                     'Notes',
                                     'FirstAddedDate',
                                     'LastUpdatedDate']
        return list(set(previous_standard_headers) - set(self.current_standard_headers()))