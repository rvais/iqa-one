import abc
import logging
import os
import posixpath

import dpath.util
import yaml

from iqa.system.command.command_base import CommandBase
from iqa.utils.exceptions import IQAConfigurationException

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union, Optional, List, Any
    from iqa.system.executor.base.execution import ExecutionBase
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.components.abstract.component import Component
    from os import PathLike

LOGGER: logging.Logger = logging.getLogger(__name__)


class Configuration(object):
    """Placeholder class of read configuration details from provided input file.
    Input file is json supported only (yaml in the future).
    """

    LOGGER = logging.getLogger(__name__)
    config_file: str = 'data_config_file'
    original_config_file: str
    local_config_dir: str  # local configuration directory (ansible inventory dir)
    node_config_dir: Union[int, str, list, dict]  # remote configuration directory
    object_list: List[Any] = []
    yaml_data: Optional[Union[dict, yaml.YAMLObject]] = None
    old_yaml_data: Optional[Union[dict, yaml.YAMLObject]] = None  # re|store configuration data

    def __init__(self, component: Component, **kwargs) -> None:
        self.component = component

        if self.config_file in kwargs.keys():
            print(kwargs.get(self.config_file))
            self.original_config_file = kwargs.get(self.config_file, None)
            self.create_configuration(self.original_config_file)
        else:
            self.create_default_configuration(**kwargs)
            LOGGER.info('No configuration file provided, using defaults')

        # Ansible synchronize must have trailing "/" to sync dir-content
        if (
            kwargs.get('inventory_dir') is not None
            and component.instance_name is not None
        ):
            self.local_config_dir = posixpath.join(
                kwargs.get('inventory_dir'),  # type: ignore
                component.instance_name,
                '',
            )
        else:
            self.local_config_dir = os.getcwd()

    def _data_getter(
        self,
        path: Union[str, PathLike],
        default: Optional[Union[int, str, list, dict]]
    ) -> Optional[Union[int, str, list, dict]]:
        """General function to query data from provided external data dictionary.

        :param path: internal path to query data (broker_xml/journal/persistence_enabled)
        :type path: str
        :param default: what to return if value not find based on key-path
        :type default: int | str | list | dict | None
        :return: found value from provided key path
        :rtype: int | str | list | dict
        """
        try:
            output: Union[int, str, list, dict] = dpath.util.get(self.yaml_data, path)
            # LOGGER.debug('Dpath_search=%s\n%s' % (path, output))
        except (KeyError, ValueError):
            LOGGER.debug('Unknown key or value %s', path)
            return default
        return output

    def load_configuration_yaml(self, path: Union[str, PathLike]) -> None:
        """Load provided configuration YAML file.

        :param path: path to configuration file
        :type path: str
        :return: List of initialized abstract servers (as objects)
        :rtype: list
        """

        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    self.yaml_data = yaml.full_load(f)
                except yaml.YAMLError:
                    raise IQAConfigurationException(
                        'Unable to load file "%s" for "%s"'
                        % (path, self.__class__.__name__)
                    )

                if 'artemis' not in self.yaml_data['render']['template']:
                    raise IQAConfigurationException(
                        'Incompatible data structure for %s !' % self.__class__.__name__
                    )

    @abc.abstractmethod
    def load_configuration(self) -> None:
        pass

    @abc.abstractmethod
    def create_configuration(self, config_file_path: Union[str, PathLike]) -> None:
        pass

    @abc.abstractmethod
    def apply_config(self, yaml_configuration: str) -> None:
        pass

    @abc.abstractmethod
    def create_default_configuration(self, **kwargs) -> None:
        pass

    def restore_config(self) -> None:
        self.apply_config(self.original_config_file)

    def copy_configuration_files(self) -> ExecutionBase:
        executor: ExecutorBase = self.component.node.executor
        args = []
        stdout = True
        stderr = True
        timeout = 20
        ansible_module = None
        ansible_args = []
        path_to_exec = None

        if executor.implementation.__contains__('ansible'):
            ansible_module='synchronize'
            ansible_args = [
                'src=%s' % self.local_config_dir,
                'dest=%s' % self.node_config_dir
            ]
        elif executor.implementation.__contains__("local"):
            path_to_exec = 'cp'
            args = ['-T', self.local_config_dir, self.node_config_dir]
        else:
            raise \
                NotImplemented("Synchronizing configuration files is not implemented for %s executor." % executor.name)

        # dump local variables into dictionary
        inputs = locals()
        # remove self and executor variables as they would mess things up
        del inputs['self']
        del inputs['executor']

        cmd: CommandBase = executor.get_preferred_command_base()(**inputs)
        return self.component.node.execute(cmd)
