import json

from .client import MessageBusClient

"""Functions for handling loading messagebus client configurations."""


def client_from_config(subconf='core', file_path='/etc/alice/bus.conf'):
    """Load messagebus configuration from file.

    The config is a basic json file with a number of "sub configurations"

    Ex:
    {
      "core": {
        "route": "/core",
        "port": "8181"
      }
      "gui": {
        "route": "/gui",
        "port": "8811"
      }
    }

    Arguments:
        subconf:    configuration to choose from the file, defaults to "core"
                    if omitted.
        file_path:  path to the config file, defaults to /etc/alice/bus.conf
                    if omitted.
    Returns:
        MessageBusClient instance based on the selected config.
    """
    with open(file_path) as f:
        conf = json.load(f)

    return MessageBusClient(**conf[subconf])
