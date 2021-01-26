from iqa.abstract.server.messaging_server import MessagingServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional  # , Union
    from iqa.abstract.listener import Listener


class Router(MessagingServer):
    """
    Abstract abstract Router
    """

    def get_url(self, port: 'Optional[int]' = None, listener: 'Optional[Listener]' = None) -> str:
        return NotImplemented

    def __init__(self, **kwargs) -> None:
        super(Router, self).__init__(**kwargs)
