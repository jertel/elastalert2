Logging
*******

By default, ElastAlert 2 uses a simple basic logging configuration to print log messages to standard error.
You can change the log level to ``INFO`` messages by using the ``--verbose`` or ``--debug`` command line options.

If you need a more sophisticated logging configuration, you can provide a full logging configuration
in the config file. This way you can also configure logging to a file, to Logstash and
adjust the logging format.

For details, see the end of ``examples/config.yaml.example`` where you can find an example logging
configuration.

