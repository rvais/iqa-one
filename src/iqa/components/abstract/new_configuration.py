import io
import logging
import os
import tempfile
from typing import TYPE_CHECKING

import yacfg
import yaml

from iqa.utils.exceptions import IQAConfigurationException

if TYPE_CHECKING:
    from typing import Union, Optional, List, Dict
    from os import PathLike


class Configuration(object):
    """Placeholder class of read configuration details from provided input file.
    Input file is json supported only (yaml in the future).
    """

    LOGGER = logging.getLogger(__name__)
    default_config_file_name: str = 'data_config_file'
    default_config_file_extension: str = 'yaml'

    def __init__(
            self,
            load_immediately: bool = False,
            config_files: 'Optional[Union[Union[str, bytes, PathLike], List[Union[str, bytes, PathLike]]]]' = None,
            profile_path: 'Optional[Union[str, bytes, PathLike]]' = None,
            output_path: 'Optional[Union[str, bytes, PathLike]]' = None,
            config_dir: 'Optional[Union[str, bytes, PathLike]]' = None,
            **kwargs
    ) -> None:
        self._config_files: Optional[
            Union[Union[str, bytes, PathLike], List[Union[str, bytes, PathLike]]]
        ] = config_files
        self._profile: Optional[Union[str, bytes, PathLike]] = profile_path
        self._config_dir: Optional[Union[str, bytes, PathLike]] = config_dir
        self._output_path: Optional[Union[str, bytes, PathLike]] = output_path

        if config_files is not None and load_immediately:
            self.load_configuration(config_files)

        self._yaml_data: Optional[Dict] = {}.update(kwargs)
        self._original_yaml_data: Optional[Dict] = None
        self._init_defaults = kwargs.copy()

    @property
    def profile(self) -> 'Optional[Union[str, bytes, PathLike]]':
        return self._profile

    @profile.setter
    def profile(self, profile: 'Optional[Union[str, bytes, PathLike]]') -> None:
        self._profile = profile

    @property
    def config_dir(self) -> 'Optional[Union[str, bytes, PathLike]]':
        return self._config_dir

    @config_dir.setter
    def config_dir(self, config_dir: 'Optional[Union[str, bytes, PathLike]]') -> None:
        self._config_dir = config_dir

    @property
    def output_path(self) -> 'Optional[Union[str, bytes, PathLike]]':
        if self._output_path is None:
            return tempfile.gettempdir()
        return self._output_path

    @output_path.setter
    def output_path(self, output_path: 'Optional[Union[str, bytes, PathLike]]') -> None:
        self._output_path = output_path

    @property
    def data(self) -> 'Dict':
        if self._yaml_data is None:
            return {}
        return self._yaml_data.copy()

    @property
    def original_data(self) -> 'Dict':
        if self._original_yaml_data is None:
            return {}
        return self._original_yaml_data.copy()

    @property
    def default_config_file(self) -> 'Union[Union[str, bytes, PathLike]]':
        return os.path.join(
            self.output_path, '%s.%s' % (self.default_config_file_name, self.default_config_file_extension)
        )

    def load_configuration(
            self,
            config_files: 'Optional[Union[Union[str, bytes, PathLike], List[Union[str, bytes, PathLike]]]]' = None
    ) -> bool:
        return self.update_configuration(True, config_files)

    def update_configuration(
            self,
            create_new_configuration: bool = False,
            config_files: 'Optional[Union[Union[str, bytes, PathLike], List[Union[str, bytes, PathLike]]]]' = None,
            **kwargs
    ) -> bool:
        if create_new_configuration:
            self._original_yaml_data = self._yaml_data
            self._yaml_data = {}

        if config_files is not None and not isinstance(config_files, list):
            config_files = [config_files]

        if config_files is None:
            config_files = []

        success = True
        for file in config_files:
            success = success and self._load_config_file(file)

        self._yaml_data.update(kwargs)

        return success

    def _load_config_file(
            self,
            config_file: 'Optional[Union[str, bytes, PathLike]]' = None
    ) -> bool:
        if config_file is None:
            return True

        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                try:
                    self._yaml_data.update(yaml.full_load(f))
                except yaml.YAMLError:
                    raise IQAConfigurationException(
                        'Unable to load file "%s" for "%s"'
                        % (config_file, self.__class__.__name__)
                    )
        return False

    def dump_configuration(
            self,
            config_file: 'Optional[Union[str, bytes, PathLike]]' = None,
            override: bool = False
    ) -> 'Optional[Union[str, bytes, os.PathLike]]':
        return self._dump_configuration(self._yaml_data, config_file, override)

    def dump_original_configuration(
            self,
            config_file: 'Optional[Union[str, bytes, PathLike]]' = None,
            override: bool = False
    ) -> 'Optional[Union[str, bytes, os.PathLike]]':
        return self._dump_configuration(self._original_yaml_data, config_file, override)

    def _dump_configuration(
            self,
            data: dict = None,
            config_file: 'Optional[Union[str, bytes, PathLike]]' = None,
            override: bool = False
    ) -> 'Optional[Union[str, bytes, os.PathLike]]':
        if data is None or len(data) == 0:
            return None

        if config_file is None:
            config_file = self.default_config_file

        exists = os.path.exists(config_file)
        if not exists or override:
            with io.FileIO(config_file, mode='w') as f:
                yaml.dump(self._yaml_data, f)
            return config_file

        return None

    def generate_config_files(
            self,
            profile_path: 'Optional[Union[str, bytes, PathLike]]' = None,
            custom_tune_files: 'Optional[Union[Union[str, bytes, PathLike], List[Union[str, bytes, PathLike]]]]' = None,
            output_path: 'Optional[Union[str, bytes, PathLike]]' = None,
            **kwqrgs
    ) -> 'Optional[Union[str, bytes, PathLike]]':
        if output_path is None:
            output_path = self.output_path

        if profile_path is None:
            profile_path = self._profile

        if not isinstance(custom_tune_files, list):
            custom_tune_files = [custom_tune_files]

        data = self._yaml_data if self._yaml_data is not None else {}

        output = yacfg.generate(
            profile=profile_path,
            output_path=output_path,
            tuning_files_list=custom_tune_files,
            tuning_data_list=[data, kwqrgs]
        )

        if output is not None:
            return output_path

        return None

    def restore_original_configuration(self) -> None:
        self._yaml_data = self.original_data
        self._original_yaml_data = None

    def create_defaults(self) -> None:
        self._create_defaults()

    def _create_defaults(self) -> None:
        self.update_configuration(True, config_files=None, kwargs=self._init_defaults)

    def __getitem__(self, k):
        if self._yaml_data is not None:
            return self._yaml_data.__getitem__(k)

    def __setitem__(self, k, v) -> None:
        if self._yaml_data is None:
            self._yaml_data = {}
        self._yaml_data.__setitem__(k, v)

    def __delitem__(self, k) -> None:
        if self._yaml_data is not None:
            self._yaml_data.__delitem__(k)

    def __len__(self) -> int:
        if self._yaml_data is not None:
            self._yaml_data.__len__()
        return 0

    def __iter__(self):
        if self._yaml_data is None:
            self._yaml_data = {}
        self._yaml_data.__iter__()

    def __contains__(self, item) -> bool:
        if self._yaml_data is not None:
            self._yaml_data.__contains__(item)
        return False
