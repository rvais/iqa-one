from enum import Enum

__all__ = ['RoutingType']


class EnumRoutingType(Enum):
    """
    Routing type
    """
    @staticmethod
    def from_value(value: str) -> 'RoutingType':
        if not value:
            return RoutingType.ANYCAST

        if value.__contains__(RoutingType.ANYCAST) and value.__contains__(RoutingType.MULTICAST):
            return RoutingType.BOTH
        elif value.__contains__(RoutingType.ANYCAST):
            return RoutingType.ANYCAST
        elif value.__contains__(RoutingType.MULTICAST):
            return RoutingType.MULTICAST
        else:
            raise ValueError('Value "%s" does not match any known type.' % value)


RoutingType = EnumRoutingType('RoutingType', [(a, a) for a in ['ANYCAST', 'MULTICAST', 'BOTH']] )
