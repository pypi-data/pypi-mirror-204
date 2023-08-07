import traceback

from autoscale_agent.util import loop_with_interval


class WorkerDispatchers:
    DISPATCH_INTERVAL = 15

    def __init__(self):
        self._dispatchers = []

    def append(self, dispatcher):
        self._dispatchers.append(dispatcher)

    def dispatch(self):
        for dispatcher in self._dispatchers:
            try:
                dispatcher.dispatch()
            except Exception as e:
                print(
                    f"Autoscale: {type(e).__name__}\n{traceback.print_tb(e.__traceback__)}"
                )

    def run(self):
        loop_with_interval(self.DISPATCH_INTERVAL, self.dispatch)
