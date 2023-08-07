import http.client
import json
import time

from autoscale_agent.util import dispatch


class WorkerDispatcher:
    def __init__(self, token, measure):
        self.token = token
        self.id = token[:7]
        self._measure = measure

    def dispatch(self):
        value = self._measure()

        if value is None:
            print(f"Autoscale[{self.id}][ERROR]: No value to dispatch (None)")
            return

        payload = {str(int(time.time())): float(value)}
        response = dispatch(body=json.dumps(payload), token=self.token)

        if not response.status == http.client.OK:
            print(
                f"Autoscale[{self.id}][ERROR]: Failed to dispatch ({response.status}) {response.read().decode()}"
            )
