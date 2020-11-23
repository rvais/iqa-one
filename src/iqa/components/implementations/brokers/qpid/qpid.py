from iqa.abstract.server.broker import Broker
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.components.protocols.amqp import AMQP10


class Qpid(ServerComponent, Broker):
    """
    Qpid broker
    A message-oriented middleware message broker written in C++ that stores, routes, and forwards messages using AMQP.
    """

    supported_protocols: list = [AMQP10()]
    name: str = 'Qpid C++ Broker'
    implementation: str = 'qpid'

    def __init__(self, name: str, **kwargs) -> None:
        super(Qpid, self).__init__(name, **kwargs)
