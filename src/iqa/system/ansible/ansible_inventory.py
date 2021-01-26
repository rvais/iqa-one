import logging

from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible.vars.manager import VariableManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Type
    from iqa.components.abstract.component import Component
    from iqa.system.node.base.node import Node
    from iqa.system.executor.base.executor import ExecutorBase


class AnsibleVirtualComponent(object):
    def __init__(
        self, name: str, cmp_type: str, implementation: str, members: list, **kwargs
    ) -> None:
        self.name: str = name
        self.cmp_type: str = cmp_type
        self.implementation: str = implementation
        self.members: list = members
        self.kwargs: dict = kwargs
        self.component: Optional[Component] = None  # real component, once created and populated with member


class AnsibleInventory(object):
    virt_component: str = 'virtual_component'

    def __init__(self, inventory: str = None, extra_vars: dict = None) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__module__)
        self.inventory: str or None = inventory
        self.loader: DataLoader = DataLoader()
        self._logger.info('Loading inventory: %s' % inventory)
        self._logger.debug('Extra variables: %s' % extra_vars)
        self.inv_mgr: InventoryManager = InventoryManager(
            loader=self.loader, sources=self.inventory
        )
        self.var_mgr: VariableManager = VariableManager(
            loader=self.loader, inventory=self.inv_mgr
        )
        self.var_mgr._extra_vars = extra_vars or dict()

    def get_hosts_containing(self, var: str = None) -> list:
        hosts: list = []

        for host in self.inv_mgr.get_hosts():
            # If no specific var provided, then add it to the list
            if not var:
                hosts.append(host)
                continue

            # If var is provided and not part of host vars, ignore it
            host_vars: dict = self.var_mgr.get_vars(host=host)
            if var not in host_vars:
                continue

            # Var has been found so adding it
            hosts.append(host)

        return hosts

    def get_hosts(self) -> 'List[Host]':
        return self.get_hosts_containing(var=None)

    def get_hosts_names(self) -> 'List[str]':
        return [x.name for x in self.get_hosts()]

    def get_host_vars(self, host: Host) -> dict:
        data: dict = self.var_mgr.get_vars(host=host)
        templar: Templar = Templar(variables=data, loader=self.loader)
        return templar.template(data, fail_on_undefined=False)

    def get_groups(self) -> 'List[Group]':
        return self.inv_mgr.groups.values()

    def get_groups_names(self) -> 'List[str]':
        groups: list = []
        for group in self.inv_mgr.get_groups_dict():
            groups.append(group)
        return groups
