"""
Represents a generic Queue entity.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.abstract.destination.routing_type import RoutingType
    from iqa.abstract.destination.address import Address


class Queue:
    def __init__(self, name: str, routing_type: 'RoutingType', address: 'Optional[Address]' = None) -> None:
        self.name: str = name
        self.routing_type: RoutingType = routing_type
        self._address: Address = address
        self.message_count: int = 0

    @property
    def fqqn(self) -> str:
        if self.address is None:
            raise ValueError("This queue haven't been assigned any address.")

        return '%s::%s' % (self.address.name, self.name)

    @property
    def address(self) -> 'Optional[Address]':
        return self._address

    @address.setter
    def set_address(self, address: 'Address') -> None:
        if self._address is not None:
            raise AttributeError("Queue %s already has assigned address %s. Address cannot be reassigned.")
        if address is None:
            raise ValueError("Expected Address object, None given.")
        self._address = address
