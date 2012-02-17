"""Test the Entity class."""

import unittest

import behaviors
from behaviors import testing


@behaviors.add("whistle")
class Whistle(object):
    def __init__(self, volume="stub"):
        self.volume = volume

    def execute(self, entity):
        pass

    def write(self, out):
        out[self.name] = {"volume": self.volume}

    def read(self, input):
        self.volume = input["whistle"]["volume"]


@behaviors.add("swim")
class Swim(object):
    def __init__(self, speed="stub"):
        self.speed = speed

    def execute(self, entity):
        pass

    def write(self, out):
        out[self.name] = {"speed": self.speed}

    def read(self, input):
        self.speed = input["swim"]["speed"]


class MockSerializer(object):
    def __init__(self):
        self.captured = {}

    def write(self, out):
        self.captured = out

    def read(self):
        return {
            "whistle": {
                "volume": "soft"
            },
            "swim": {
                "speed": 11.0
            }
        }


class TestEntity(unittest.TestCase):
    def test_it_should_map_events_to_methods(self):
        """Entities should map method calls to behaviors."""
        stub_behavior = testing.StubBehavior()

        # Map the "do_it" method to stub_behavior.execute().
        stub_behaviors = {"do_it": stub_behavior}
        stub_entity = behaviors.Entity(stub_behaviors, None)
        stub_entity.do_it()

        self.assertTrue(stub_behavior.capture["called"])

    def test_it_should_pass_parameters_to_the_behavior(self):
        """Parameters passed to the method should be passed to the behavior.

        """
        stub_behavior = testing.StubBehavior()
        stub_behaviors = {"poke": stub_behavior}
        stub_entity = behaviors.Entity(stub_behaviors, None)

        stub_entity.poke("everything", 42, nisi="fun", non=False)

        self.assertTrue("parameters" in stub_behavior.capture)
        captured_parameters = stub_behavior.capture["parameters"]
        self.assertTrue(42 in captured_parameters["args"])
        self.assertTrue("everything" in captured_parameters["args"])
        self.assertTrue("nisi" in captured_parameters["kwargs"])
        self.assertEqual("fun", captured_parameters["kwargs"]["nisi"])
        self.assertTrue("non" in captured_parameters["kwargs"])

        self.assertEqual(False, captured_parameters["kwargs"]["non"])

    def test_write(self):
        """When an Entity is written, it should delegate to it's
        serialization strategy.

        """
        serializer = MockSerializer()
        entity = behaviors.Entity(
            behaviors={
                Whistle.name: Whistle(volume="loud"),
                Swim.name: Swim(speed=10.0)
            },
            serializer=serializer)

        entity.write()

        self.assertTrue("whistle" in serializer.captured)
        self.assertTrue("volume" in serializer.captured["whistle"])
        self.assertEqual("loud", serializer.captured["whistle"]["volume"])

        self.assertTrue("swim" in serializer.captured)
        self.assertTrue("speed" in serializer.captured["swim"])
        self.assertEqual(10.0, serializer.captured["swim"]["speed"])

    def test_read(self):
        """When an Entity is written, it should delegate to it's
        serialization strategy.

        """
        whistle = Whistle()
        swim = Swim()
        serializer = MockSerializer()
        entity = behaviors.Entity(
            behaviors={Whistle.name: whistle, Swim.name: swim},
            serializer=serializer)

        entity.read()

        self.assertEqual("soft", whistle.volume)
        self.assertEqual(11.0, swim.speed)
