"""A Entity is an object which contains a collection of Behaviors. Behaviors
respond to events, i.e. method calls on the Entity.

"""

import logging


class Entity(object):
    def __init__(self, behaviors, serializer):
        logging.debug("Initializing Entity with behaviors (%s).", behaviors)
        self._behaviors = behaviors
        self._serializer = serializer

    def __getattr__(self, name):
        """Try to use a Behavior before allowing normal attribute access.

        """
        logging.debug(
            "Searching for (%s) in Behaviors (%s).", name, self._behaviors)
        behavior = self._behaviors.get(name)
        if behavior:
            logging.debug("Found Behavior (%s).", behavior.__class__)

            def call_with_entity(*args, **kwargs):
                return behavior.execute(self, *args, **kwargs)
            return call_with_entity

        raise AttributeError(
            "(%s) was not found as a normal attribute, method or behavior." %
            (name))

    def write(self):
        """Generate a representation of this entity's current state."""
        out = {}
        for behavior in self._behaviors.values():
            behavior.write(out)
        self._serializer.write(out)

    def read(self):
        """Read a representation of this entity's state."""
        input = self._serializer.read()
        for behavior in self._behaviors.values():
            behavior.read(input)
