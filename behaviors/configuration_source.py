"""Defines the interface for configuration sources.

Configuration sources fetch entity configurations from sources such as a YAML
file or database.

"""

import abc


class ConfigurationSource(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fetch(self, name):
        """ConfigurationSources should implement this method to return the
        configuration identified by ``name``.

        """
        pass
