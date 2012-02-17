"""The factory manager holds factories. Factories objects are classes or
methods that responds to a ``create()`` call.

Factories are added to the FactoryManager with ``register()``. Concrete
products are created with ``create()``.

Example::

    # Register factories with the factory manager.
    factory_manager = FactoryManager()
    factory_manager.register("wibble", WibbleFactory())

    # Create wibbles.
    small_wibbles = factory_manager.create("wibble", size="small")

This pattern is particularly powerful when a body of code is responsible
for creating objects but their types are only known at runtime (from
configuration, database queries or request bodies).

Example::

    # Given a request_body dict and a factory manager with registered
    # factories.
    product_type = request_body.get("type")

    # Create a product of some unknown type and use it.
    product = factory_manager.create(product_type)
    product.execute_responsibility(request_body.get("configuration"))

Of course, a system such as this requires you design your software to act on
interfaces and not implementations. This is something that you should be doing
regardless of your choice in creational patterns.

For more information on creational patterns and programming to an interface
not an implementation, see Gamma, Erich et al. (1995), Design Patterns:
Elements of Reusable Object-Oriented Software, Boston, Addison-Wesley, 1st ed.

"""

import logging


class FactoryManager(object):
    """The factory manager is responsible for collecting binding tags and
    creating objects with the bound factories.

    """
    def __init__(self):
        self._factories = {}

    def register(self, tag, factory):
        """Associate a tag with a factory or type so it can be created later.

        """
        binding = self._factories.get(tag)
        if binding:
            _report_error(
                "Tag (%s) already bound to type (%s)." % (tag,
                binding.__class__))

        logging.debug(
            "Binding tag (%s) to type (%s).", tag, factory.__name__)
        self._factories[tag] = factory

    def create(self, tag, *args, **kwargs):
        """Create a type identified by tag."""
        factory = self._factories.get(tag)
        if not factory:
            _report_error("No binding exists for tag (%s)" % (tag))

        logging.debug(
            "Creating (%s) from factory (%s).", tag, factory.__name__)
        if hasattr(factory, "create"):
            return factory.create(*args, **kwargs)
        return factory(*args, **kwargs)


def _report_error(message):
    logging.warning(message)
    raise NameError(message)
