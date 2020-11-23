from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Union
    from iqa.abstract.destination.routing_type import RoutingType
    from iqa.abstract.destination.queue import Queue


class Address:
    """
    Address class
    """

    def __init__(
        self,
        name: str,
        routing_type: RoutingType,
        queues: Optional[Union[Queue, List[Queue]]] = None
    ) -> None:
        self.name: str = name
        self.routing_type: RoutingType = routing_type
        self._queues: List[Queue]
        if isinstance(queues, list):
            self._queues = queues.copy()
        elif queues is None:
            self._queues = list()
        else:
            self._queues = [queues]

    @property
    def queues(self) -> list:
        return self._queues.copy()

    def add_queue(self, queue: Queue) -> None:
        self._queues.append(queue)

    def has_queue(self, queue: Union[Queue, str]) -> bool:
        if isinstance(queue, str):
            for q in self._queues:
                if q.name == queue:
                    return True
            return False
        return queue in self._queues

