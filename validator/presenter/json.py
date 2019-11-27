import json


class JsonResultPresenter:

    def __init__(self, result):
        self.result = result

    def __str__(self):
        return json.dumps(self.result.to_dict())
