"""A Behavior responds to stimulus with it's ``execute`` method. Behaviors are
collected by Entities.

"""

import abc


class Behavior(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, entity, *args, **kwargs):
        """Behaviors should implement this method to perform the duty of the
        behavior.

        """
        pass

    @abc.abstractmethod
    def write(self, output):
        """Behaviors should implement this method to generate a dict
        representing the current state of the behavior.

        """
        pass

    @abc.abstractmethod
    def read(self, input):
        """Behaviors should implement this method to read a dict representing
        the state of this behavior.

        """
        pass


def add(name):
    """Helper to ready a class to be used as a behavior."""
    def wrapper(behavior_class):
        """Add a class level name attribute and sub class the Behavior base
        class which defines the required interface for a Behavior.
        """
        if not name:
            raise ValueError("Behaviors require a valid name.")

        class BehaviorWrapper(behavior_class, Behavior, object):
            pass
        behavior_class.name = name
        return BehaviorWrapper

    return wrapper
