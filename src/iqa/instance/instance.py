"""
IQA instance which is populated based on an ansible compatible inventory file.
"""
import logging
import os

from iqa.components.implementations.component_factory import ComponentFactory
from iqa.system.ansible.ansible_inventory import AnsibleInventory
from iqa.system.executor.executor_factory import ExecutorFactory
from iqa.system.node.node_factory import NodeFactory
from iqa.system.service.service_factory import ServiceFactory

from ansible.inventory.host import Host
from ansible.inventory.group import Group

from iqa.abstract.client.client import Client
from iqa.abstract.client.receiver import Receiver
from iqa.abstract.client.sender import Sender
from iqa.abstract.server.broker import Broker
from iqa.abstract.server.router import Router

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union, List, Dict
    from iqa.components.abstract.component import Component
    from iqa.system.node.base.node import Node
    from iqa.system.executor.base.executor import ExecutorBase

logger = logging.getLogger(__name__)


class Instance:
    """IQA helper class

    Store variables, node and related things
    """

    def __init__(self, inventory: str = '', cli_args: 'Dict' = None) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__module__)
        self.inventory: str = inventory
        self._inv_mgr: AnsibleInventory = AnsibleInventory(
            inventory=self.inventory, extra_vars=cli_args
        )
        self._nodes: List[Node] = []
        self._components: List[Component] = []

        self._load_components()

    def _load_components(self) -> None:
        """
        Parses the mandatory Ansible inventory file and load all defined
        messaging components.
        :return:
        """

        def get_and_remove_key(vars_dict: dict, key: str, default: str = None) -> str:
            val: str = vars_dict.get(key, default)
            if key in vars_dict:
                del vars_dict[key]
            return val

        # Loading all hosts that provide the component variable
        inventory_hosts: List[Host] = self._inv_mgr.get_hosts()
        inventory_groups: List[Group] = self._inv_mgr.get_groups()
        nodes = {}

        defaults: Dict = {
            'executor': 'local',
            'ansible_host': '127.0.0.1',
            'port': 22,
            'ansible_user': os.environ['USER'],
            # '': '',
        }

        node_vars: Dict = defaults.copy()

        for group in inventory_groups:
            node_vars.update(group.vars)
            if group.name in ['all', 'ungrouped']:
                continue

            for host in group.hosts:
                node_vars.update(host.get_vars())

                if host.name not in nodes.keys():
                    args: Dict = node_vars.copy()
                    del args['implementation']
                    del args['executor']
                    del args['ansible_user']

                    executor = ExecutorFactory.create_executor(
                        implementation=node_vars['executor'],
                        user=node_vars['ansible_user'],
                        **args
                    )

                    args: Dict = node_vars.copy()
                    del args['executor']
                    del args['ansible_host']

                    node = NodeFactory.create_node(host.name, ip=node_vars['ansible_host'], executor=executor, **args)
                    nodes[host.name] = node

                component: Component = ComponentFactory.create_specified_component(
                    component_type=group.name,
                    node=nodes[host.name],
                    **node_vars
                )
                self.new_component(component)

        self._nodes = nodes.items()

    def new_node(
        self, hostname: str, executor_impl: str = 'ansible', ip: str = None, **kwargs
    ) -> 'Node':
        """Create new node under iQA instance

        :param executor_impl:
        :type executor_impl:
        :param hostname:
        :type hostname:
        :param ip:
        :type ip:

        :return:
        :rtype:
        """
        executor: ExecutorBase = ExecutorFactory.create_executor(implementation=executor_impl, **kwargs)

        # Create the Node for current client
        node: Node = NodeFactory.create_node(
            hostname=hostname, executor=executor, ip=ip, **kwargs
        )

        self._nodes.append(node)
        return node

    def new_component(self, component) -> 'Component':
        """Create new component in IQA instance

        :param component:
        :type component:

        :return:
        :rtype:
        """
        self.components.append(component)
        return component

    @property
    def nodes(self) -> 'List[Node]':
        return self._nodes.copy()

    @property
    def components(self) -> 'List[Component]':
        return self._components.copy()

    @property
    def brokers(self) -> 'List[Broker]':
        """
        Get all broker instances on this node
        :return:
        """
        return [
            component for component in self._components if isinstance(component, Broker)
        ]

    @property
    def clients(self) -> 'List[Client]':
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        return [
            component for component in self._components if isinstance(component, Client)
        ]

    def get_clients(
        self, client_type: type, implementation: str = ''
    ) -> 'List[Client]':
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        component: Client
        return [
            component
            for component in self.clients
            if isinstance(component, client_type)
            and (
                implementation == ''
                or getattr(component, 'implementation', '').lower() == implementation.lower()
            )
        ]

    def get_receiver(self, hostname: str) -> 'Optional[Receiver]':
        """
        Return a single receiver running on provided hostname.
        :param hostname:
        :return: the receiver implementation running on given host
                 or None otherwise.
        """
        # receiver: Optional['ClientType']
        receiver: Union[Receiver, Client, Component]
        for receiver in self.get_clients(client_type=Receiver):
            if receiver.node is not None and receiver.node.hostname == hostname:
                return receiver

        return None

    def get_sender(self, hostname: str) -> 'Optional[Sender]':
        """
        Return a single sender running on provided hostname.
        :param hostname:
        :return: the sender implementation running on given host
                 or None otherwise.
        """
        sender: Union[Sender, Client, Component]
        for sender in self.get_clients(client_type=Sender):
            if sender.node is not None and sender.node.hostname == hostname:
                return sender

        return None

    @property
    def routers(self) -> 'List[Router]':
        """
        Get all router instances on this node
        :return:
        """
        return [
            component for component in self._components if isinstance(component, Router)
        ]

    def get_routers(self, hostname: str = None) -> 'List[Router]':
        """
        Get all router instances on this node
        :type hostname: optional hostname
        :return:
        """
        results: List[Router] = []
        router: Union[Router, Component]

        for router in self.routers:
            if router.node is not None and router.node.hostname == hostname:
                results.append(router)

        return results

    def get_brokers(self, hostname: str = None):
        """
        Get all broker instances on this node
        :type hostname: optional hostname
        :return:
        """
        results: List[Broker] = []
        broker: Union[Broker, Component]

        for broker in self.brokers:
            if broker.node is not None and broker.node.hostname == hostname:
                results.append(broker)

        return results
