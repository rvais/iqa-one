from typing import TYPE_CHECKING
from iqa.components.abstract.new_configuration import Configuration
import os

if TYPE_CHECKING:
    from typing import Union, Optional, List, Dict
    from os import PathLike


class ArtemisConfig(Configuration):
    """Placeholder class of read configuration details for Artemis/AMQ 7
    from provided input file.
    Input file is json supported only (yaml in the future).

    This class is directly tied to ExternalBroker.
    """

    DEFAULT_HOME: str = '/opt/artemis_2.16'
    DEFAULT_INSTANCE_HOME: str = '/opt/artemis_i0'
    DEFAULT_INSTANCE_NAME: str = 'artemis'

    PROFILE_PATH_FORMAT: str = 'amq_broker/%s/%s.yaml.jinja2'
    DEFAULT_VERSION: str = '2.16'
    DEFAULT_PROFILE_NAME: str = 'default'
    DEFAULT_TUNING_FILE: str = 'artemis_defaults'

    def __init__(
        self,
        amq_version: str = DEFAULT_VERSION,
        profile_name: str = DEFAULT_PROFILE_NAME,
        profile_path_format: str = PROFILE_PATH_FORMAT,
        broker_name: str = DEFAULT_INSTANCE_NAME,
        broker_home: 'Optional[Union[str, bytes, PathLike]]' = DEFAULT_HOME,
        broker_instance: 'Optional[Union[str, bytes, PathLike]]' = DEFAULT_INSTANCE_HOME,
        load_immediately: bool = False,
        config_files: 'Optional[Union[Union[str, bytes, PathLike], List[Union[str, bytes, PathLike]]]]' = None,
        profile_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        output_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        config_dir: 'Optional[Union[str, bytes, PathLike]]' = None,
        **kwargs
    ) -> None:
        if profile_path is None:
            profile_path = profile_path_format % (amq_version, profile_name)

        # dump arguments into dictionary
        inputs = locals()
        # remove self, kwargs and some variables as they would mess things up
        del inputs['self']
        del inputs['kwargs']
        del inputs['amq_version']
        del inputs['profile_name']
        del inputs['profile_path_format']
        # update kwargs to pass in super().__init__()
        kwargs.update(inputs)

        super(ArtemisConfig, self).__init__(**kwargs)

        self._broker_home = broker_home
        self._instance_config: str = os.path.join(broker_instance, 'etc')
        self._instance_bin: str = os.path.join(broker_instance, 'bin')
        self._instance_executable: str = os.path.join(broker_instance, 'bin', 'artemis')

    def _create_defaults(self) -> None:
        super(ArtemisConfig, self)._create_defaults()

    @property
    def default_config_file(self) -> 'Union[str, bytes, PathLike]':
        return os.path.join(
            self.output_path, '%s.%s' % (self.DEFAULT_TUNING_FILE, self.default_config_file_extension)
        )
