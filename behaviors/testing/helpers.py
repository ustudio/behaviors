"""Helper module for testing FEB objects."""

from behaviors import behavior


class StubBehavior(behavior.Behavior):
    def __init__(self, capture=dict()):
        self.capture = capture

    def execute(self, *args, **kwargs):
        self.capture["called"] = True
        self.capture["parameters"] = {
            "args": [arg for arg in args],
            "kwargs": dict([(key, value) for key, value in kwargs.items()])
        }

    def write(self, output):
        pass

    def read(self, input):
        pass
