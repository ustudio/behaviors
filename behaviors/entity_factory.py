"""The EntityFactory is responsible for creating Entities from configurations
and attaching Behaviors to them.

"""

import logging

from entity import Entity


class EntityFactory(object):
    def __init__(
            self, configuration_source, behavior_factory, serializer_factory):
        self._configuration_source = configuration_source
        self._behavior_factory = behavior_factory
        self._serializer_factory = serializer_factory

    def create(self, entity_name):
        """Create an Entity from the entity_name.

        The Entity's configuration will be extracted from the configuration
        source. Any Behaviors defined in the configuration will be constructed
        and attached to it.

        """
        entity_configuration = self._configuration_source.fetch(entity_name)

        behavior_configurations = entity_configuration.get("behaviors")
        if not behavior_configurations:
            _configuration_error(
                "Entity configuration (%s) requires behaviors "
                "configurations." % (entity_name))

        behaviors = {}
        for configuration in behavior_configurations:
            behavior_name = configuration.get("name")
            if not behavior_name:
                _configuration_error(
                    "Behavior configuration (%s) requires a name attribute." %
                    (configuration))
            behavior = self._behavior_factory.create(behavior_name)
            behaviors[behavior_name] = behavior

        serializer_configuration = entity_configuration.get("serializer")
        if not serializer_configuration:
            _configuration_error(
                "Entity configuration (%s) requires a serializer "
                "configuration." % (entity_name))
        serializer_name = serializer_configuration.get("name")
        serializer = self._serializer_factory.create(serializer_name)

        return Entity(behaviors=behaviors, serializer=serializer)


class ConfigurationError(Exception):
    """Raised when a configuration is missing a required parameter."""
    pass


def _configuration_error(message):
    logging.warning(message)
    raise ConfigurationError(message)
