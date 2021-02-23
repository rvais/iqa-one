"""
Object representing group in ansible inventory.
"""
import logging

from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible.vars.manager import VariableManager

logger = logging.getLogger(__name__)


class InventoryGroup(object):

    def __init__(self, name: str, hosts: list = None, vars: dict = None):
        self.name: str = None
        self.hosts: list = []
        self.vars: dict = {}
        self.name = name
        if vars is not None and isinstance(vars, dict):
            self.vars.update(vars)
        if hosts is not None and isinstance(hosts, list):
            self.hosts.extend(hosts)

    @property
    def get_hosts(self):
        return self.hosts.copy();

    @property
    def get_vars(self):
        return self.vars.copy()