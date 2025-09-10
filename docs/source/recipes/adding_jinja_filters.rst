.. _custom jinja2 filters:

Custom Jinja2 Filters
=====================

`Jinja2 filters <https://jinja.palletsprojects.com/en/stable/api/#writing-filters>`_ are functions that allow you to modify variables in Jinja2 templates.
ElastAlert 2 supports default Jinja2 filters out of the box, but you can also create your own custom filter functions and use them in alert templates.
This is useful if you want to perform specific transformations that are not available in the built-in Jinja2 filters.

To create a custom Jinja2 filter, you need to instruct ElastAlert to load it by specifying the ``jinja_filters`` option in your rule configuration file.

.. code-block:: yaml

    # rules/my-rule.yaml
    jinja_filters:
      - module.file.ClassName
      - module.otherfile.OtherClassName

The value of ``jinja_filters`` should be a list of strings, where each item specifies the module, file, and class name containing the filter functions.

Example: ``filters.domain.DomainFilters`` would load the ``DomainFilters`` class from the ``domain.py`` file in the ``filters`` module (``filters/domain.py``).

The module and class names can be arbitrary (but it needs to be on the load path). The class should contain one or more
static methods that begin with `filter_`. Each of these methods will be registered as a Jinja2 filter, with the name being the method name without the `filter_` prefix.

The loading of filters is global - any rule file can load a filter, and once loaded, the filter is available from all rules.
Avoid loading race conditions by making sure any rule that depends on a custom filter also loads it.

Example
-------

Let's create a custom filter that defangs links by replacing `.` (dot) with `[.]` in URL-s. First, create a modules folder for the filter in the ElastAlert 2 directory.

.. code-block:: console

    $ mkdir filters
    $ cd filters
    $ touch __init__.py

Then, write the filter class. All methods starting with `filter_` will be registered as Jinja2 filters.

.. code-block:: python

    # filters/domain.py
    class DomainFilters:

        @staticmethod
        def filter_defang(value):
            """Replaces '.' with '[.]' in links to defang dangerous links."""
            if not isinstance(value, str):
                return value
            return value.replace(".", "[.]")

Now, let's load the filter and use it in an alert template.

.. code-block:: yaml

    # rules/link-rules.yaml
    name: dangerous-link
    type: any

    filter:
      - query:
          query_string:
            query: >
              event.category:"dangerouse_network_activity"

    jinja_filters:
      - jinja.filters.Domain

    alert_text: |
      Found a dangerous URL from network logs: `{{ url.original | defang }}`
