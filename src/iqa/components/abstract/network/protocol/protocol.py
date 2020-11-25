from enum import Enum
from types import DynamicClassAttribute
from collections import namedtuple

__all__ = ['Protocol']

ProtocolObject = namedtuple('ProtocolObject', 'name port')


class EnumProtocol(ProtocolObject, Enum):

    @DynamicClassAttribute
    def port(self):
        """The value of the Enum member."""
        return self._value_.port


protocol_list = [
    ("CORE", 5446),
    ("AMQP10", 5672),
    ("AMQP", 61616),
    ("MQTT", 1883),
    ("STOMP", 61613),
    ("Openwire", 61617)
]

Protocol = EnumProtocol('Protocol', [(protocol, (protocol, port)) for protocol, port in protocol_list])


# from abc import ABC, abstractmethod
# from typing import Any
#
#
# class Protocol(ABC):
#     """Protocol abstraction"""
#
#     @abstractmethod
#     @property
#     def name(self) -> str:
#         raise NotImplementedError
#
#     @abstractmethod
#     @property
#     def default_port(self) -> int:
#         raise NotImplementedError
#
#     @abstractmethod
#     @property
#     def transport(self) -> Any:
#         raise NotImplementedError
