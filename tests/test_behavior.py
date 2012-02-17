"""Test the Behavior class."""

import re
import unittest

import behaviors


@behaviors.add("zipcode")
class ZipCodeValidator(object):
    def execute(self, entity, zip_code):
        zip_code_re = re.compile("^\d{5}$")
        if zip_code_re.match(unicode(zip_code)):
            return True
        return False

    def write(self, output):
        pass

    def read(self, input):
        pass


@behaviors.add("mock")
class MockBehavior(object):
    def __init__(self, value):
        self._value = value

    def execute(self, entity, value):
        self._value = value

    def write(self, output):
        output[self.name] = {"value": self._value}

    def read(self, input):
        pass


class DummyEntity(object):
    pass


class TestAddBehaviors(unittest.TestCase):
    def test_add_behavior(self):
        """The add behavior helper should setup a class as a valid behavior.

        """
        @behaviors.add("stub")
        class StubBehavior(object):
            def execute(self, entity):
                pass

            def write(self, output):
                pass

            def read(self, input):
                pass

        stub_behavior = StubBehavior()

        self.assertEqual("stub", StubBehavior.name)
        self.assertTrue(isinstance(stub_behavior, StubBehavior))
        self.assertTrue(isinstance(stub_behavior, behaviors.Behavior))
        self.assertTrue(isinstance(stub_behavior, object))


class TestBehavior(unittest.TestCase):
    def test_it_runs_the_behavior(self):
        """It runs the Behavior's execute method with expected results. This
        example validates zip codes.

        """
        entity = behaviors.Entity(
            behaviors={"validate": ZipCodeValidator()}, serializer=None)

        self.assertTrue(entity.validate(zip_code=86753))
        self.assertFalse(entity.validate(zip_code=2))

    def test_it_writes(self):
        """The Behavior should serialize itself correctly.

        It is created with an initial data value and after execution it should
        serialize an updated value.

        """
        behavior = MockBehavior(42)
        output = {}
        behavior.write(output)
        self.assertTrue(MockBehavior.name in output)
        self.assertEqual(42, output[MockBehavior.name]["value"])

        behavior.execute(DummyEntity(), 84)
        behavior.write(output)
        self.assertEqual(84, output[MockBehavior.name]["value"])
