"""
Send offers a simple entry point for scripts to send a single  message on
the alice messagebus.

A bash script can run

python -c "from alice_bus_client.send_func import send; \
send('speak', {'utterance': 'hello'})"
"""
from websocket import create_connection

from .client import MessageBusClient
from .message import Message


def send(message_to_send, data_to_send=None, config=None):
    """Send a single message over the websocket.

    Args:
        message_to_send (str): Message to send
        data_to_send (dict): data structure to go along with the
            message, defaults to empty dict.
    """
    data_to_send = data_to_send or {}

    url = MessageBusClient.build_url(config.get("host"),
                                     config.get("port"),
                                     config.get("route"),
                                     config.get("ssl"))

    # Send the provided message/data
    ws = create_connection(url)
    packet = Message(message_to_send, data_to_send).serialize()
    ws.send(packet)
    ws.close()
