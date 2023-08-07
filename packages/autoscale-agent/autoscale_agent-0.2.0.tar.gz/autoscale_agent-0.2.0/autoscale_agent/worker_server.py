import json


class WorkerServer:
    def __init__(self, token, measure):
        self.token = token
        self._measure = measure

    def serve(self):
        value = self._measure()

        if value is None:
            return json.dumps(value)
        else:
            return json.dumps(str(value))
