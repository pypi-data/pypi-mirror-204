"""
Small utils and tools to use with the Messagebus.
"""
import json
import logging


def create_echo_function(name):
    """Standard logging mechanism for Alice processes.

    This creats
    Arguments:
        name (str): Reference name of the process

    Returns:
        func: The echo function
    """
    log = logging.getLogger(name)

    def echo(message):
        try:
            msg = json.loads(message)
            msg_type = msg.get("type", "")
            # do not log tokens from registration messages
            if msg_type == "registration":
                msg["data"]["token"] = None
                message = json.dumps(msg)
        except Exception as exc:
            log.info("Error: %s", repr(exc), exc_info=True)

        # Listen for messages and echo them for logging
        log.info("BUS: %s", repr(message))
    return echo
