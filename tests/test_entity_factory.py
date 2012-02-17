"""Test the EntityFactory class."""

import unittest

import behaviors
from behaviors import testing


class StubConfigurationSource(behaviors.ConfigurationSource):
    """Return stub configuration data."""
    def fetch(self, name):
        return {
            "behaviors": [{
                "name": "stub"
            }],
            "serializer": {
                "name": "stub"}
        }


class StubSerializer(object):
    def __init__(self, capture):
        self._capture = capture

    def write(self, output):
        self._capture["serializer_write"] = True

    def read(self):
        self._capture["serializer_read"] = True


class TestEntityFactory(unittest.TestCase):
    def setUp(self):
        super(TestEntityFactory, self).setUp()
        self._capture = {}
        self._behavior_factory = behaviors.FactoryManager()
        self._behavior_factory.register("stub", self._make_stub_behavior)
        self._serializer_factory = behaviors.FactoryManager()
        self._serializer_factory.register("stub", self._make_mock_serializer)

    def test_entity_construction(self):
        """It should create an entity from the given name."""
        configuration_source = StubConfigurationSource()
        factory = behaviors.EntityFactory(
            configuration_source=configuration_source,
            behavior_factory=self._behavior_factory,
            serializer_factory=self._serializer_factory)
        entity = factory.create("stub_entity")
        self.assertIsNotNone(entity)

    def test_entity_responds_to_event(self):
        """The new entity should respond to the given event."""
        factory = behaviors.EntityFactory(
            configuration_source=StubConfigurationSource(),
            behavior_factory=self._behavior_factory,
            serializer_factory=self._serializer_factory)
        entity = factory.create("stub_entity")
        entity.stub()
        self.assertTrue(self._capture["called"])

    def test_write_entity(self):
        """The entity should write itself."""
        factory = behaviors.EntityFactory(
            configuration_source=StubConfigurationSource(),
            behavior_factory=self._behavior_factory,
            serializer_factory=self._serializer_factory)
        entity = factory.create("stub_entity")
        entity.write()

        self.assertTrue("serializer_write" in self._capture)

    def test_read_entity(self):
        """The entity should read itself."""
        factory = behaviors.EntityFactory(
            configuration_source=StubConfigurationSource(),
            behavior_factory=self._behavior_factory,
            serializer_factory=self._serializer_factory)
        entity = factory.create("stub_entity")
        entity.read()

        self.assertTrue("serializer_read" in self._capture)

    def _make_stub_behavior(self):
        stub_behavior = testing.StubBehavior(self._capture)
        return stub_behavior

    def _make_mock_serializer(self):
        stub_serializer = StubSerializer(self._capture)
        return stub_serializer
