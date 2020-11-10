"""
IQA instance which is populated based on an ansible compatible inventory file.
"""
import logging
from typing import List, Optional, Union, TYPE_CHECKING

from iqa.components.brokers import BrokerFactory
from iqa.components.clients.external import ClientFactory
from iqa.components.routers import RouterFactory
from iqa.system.ansible.ansible_inventory import AnsibleInventory
from iqa.system.executor import ExecutorFactory
from iqa.system.node import NodeFactory
from iqa.system.service import ServiceFactory

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from iqa.utils.types import (
        BrokerType,
        ClientType,
        ComponentType,
        ExecutorType,
        NodeType,
        RouterType,
        ReceiverSubtype,
        SenderSubtype,
    )
else:
    from iqa.abstract.client.client import Client
    from iqa.abstract.server.broker import Broker
    from iqa.abstract.server.router import Router
    from iqa.components.abstract.component import Component
    from iqa.system.executor.executor import ExecutorBase
    from iqa.system.node.node import Node


class Instance:
    """IQA helper class

    Store variables, node and related things
    """

    def __init__(self, inventory: str = '', cli_args: dict = None) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__module__)
        self.inventory: str = inventory
        self._inv_mgr: AnsibleInventory = AnsibleInventory(
            inventory=self.inventory, extra_vars=cli_args
        )
        self.nodes: List['NodeType'] = []
        self.components: List[
            Optional[Union['ComponentType', 'ClientType', 'BrokerType', 'RouterType']]
        ] = []

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
        inventory_hosts: list = self._inv_mgr.get_hosts_containing(var='component')
        nodes: List['NodeType'] = []

        for cmp in inventory_hosts:
            component: Optional[Union[Component, Client, Broker, Router]]
            # Make a shallow copy (important as retrieved keys are deleted)
            # print('ansible host = %s' % cmp)
            cmp_vars: dict = dict(self._inv_mgr.get_host_vars(host=cmp))

            # Common variables across all component types
            cmp_type: str = get_and_remove_key(cmp_vars, 'component')
            cmp_impl: str = get_and_remove_key(cmp_vars, 'implementation')
            cmp_exec: str = get_and_remove_key(cmp_vars, 'executor', 'ansible')
            cmp_ip: str = cmp_vars.get('ansible_host', None)

            # Getting the executor instance
            executor: 'ExecutorType' = ExecutorFactory.create_executor(
                exec_impl=cmp_exec, **cmp_vars
            )

            # Create the Node for current client
            node: Node = NodeFactory.create_node(
                hostname=cmp.name, executor=executor, ip=cmp_ip
            )
            nodes.append(node)

            # Now loading variables that are specific to each component
            if cmp_type == 'client':
                # Add list of clients into component list
                cmp_list: List[
                    Union[Component, Client, Broker, Router]
                ] = ClientFactory.create_clients(
                    implementation=cmp_impl, node=node, executor=executor, **cmp_vars
                )

                for client in cmp_list:
                    self.new_component(client)

            elif cmp_type in ['router', 'broker']:
                component = None
                # A service name is expected
                cmp_svc: str = get_and_remove_key(cmp_vars, 'service')
                svc = ServiceFactory.create_service(
                    executor=executor, service_name=cmp_svc, **cmp_vars
                )

                if cmp_type == 'router':
                    component = RouterFactory.create_router(
                        implementation=cmp_impl,
                        node=node,
                        executor=executor,
                        service_impl=svc,
                        **cmp_vars
                    )

                elif cmp_type == 'broker':
                    component = BrokerFactory.create_broker(
                        implementation=cmp_impl,
                        node=node,
                        executor=executor,
                        service_impl=svc,
                        **cmp_vars
                    )

                self.new_component(component)

        self.nodes = nodes

    # TODO: @dlenoch re-implement node logic
    def new_node(
        self, hostname: str, executor_impl: str = 'ansible', ip: str = None
    ) -> 'NodeType':
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
        executor: ExecutorBase = ExecutorFactory.create_executor(implementation=executor_impl)

        # Create the Node for current client
        node: Node = NodeFactory.create_node(
            hostname=hostname, executor=executor, ip=ip
        )
        self.nodes.append(node)
        return node

    def new_component(
        self,
        component: Union['ComponentType', 'ClientType', 'BrokerType', 'RouterType'],
    ) -> Union['ComponentType', 'ClientType', 'BrokerType', 'RouterType']:
        """Create new component in IQA instance

        :param component:
        :type component:

        :return:
        :rtype:
        """
        self.components.append(component)
        return component

    @property
    def brokers(self) -> List['BrokerType']:
        """
        Get all broker instances on this node
        :return:
        """
        return [
            component for component in self.components if isinstance(component, Broker)
        ]

    @property
    def clients(self) -> List['ClientType']:
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        return [
            component for component in self.components if isinstance(component, Client)
        ]

    def get_clients(
        self, client_type: type, implementation: str = ''
    ) -> List['ClientType']:
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
                or component.implementation == implementation.lower()
            )
        ]

    def get_receiver(self, hostname: str) -> Optional['ClientType']:
        """
        Return a single receiver running on provided hostname.
        :param hostname:
        :return: the receiver implementation running on given host
                 or None otherwise.
        """
        # receiver: Optional['ClientType']
        receiver: Component
        for receiver in self.get_clients(client_type=ReceiverSubtype):
            if not isinstance(receiver, Client):
                if receiver.node.hostname == hostname:
                    return receiver

        return None

    def get_sender(self, hostname: str) -> Optional['ClientType']:
        """
        Return a single sender running on provided hostname.
        :param hostname:
        :return: the sender implementation running on given host
                 or None otherwise.
        """
        sender: Optional['ClientType']
        for sender in self.get_clients(client_type=SenderSubtype):
            if not isinstance(sender, Client):
                if sender.node.hostname == hostname:
                    return sender

        return None

    @property
    def routers(self) -> List['RouterType']:
        """
        Get all router instances on this node
        :return:
        """
        return [
            component for component in self.components if isinstance(component, Router)
        ]

    def get_routers(self, hostname: str = None) -> List['RouterType']:
        """
        Get all router instances on this node
        :type hostname: optional hostname
        :return:
        """
        return [
            component
            for component in self.routers
            if not hostname
            or (
                not isinstance(component, Router)
                and component.node.hostname == hostname
            )
        ]

    def get_brokers(self, hostname: str = None) -> List['BrokerType']:
        """
        Get all broker instances on this node
        :type hostname: optional hostname
        :return:
        """
        return [
            component
            for component in self.brokers
            if not hostname
            or (
                not isinstance(component, Broker)
                and component.node.hostname == hostname
            )
        ]
