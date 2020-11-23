from iqa.components.abstract.configuration import Configuration
from iqa.components.abstract.server.server_component import ServerComponent


class RouterConfiguration(Configuration):
    def __init__(self, component: ServerComponent, **kwargs) -> None:
        super(RouterConfiguration, self).__init__(component, **kwargs)

    def apply_config(self, configuration: str) -> None:
        pass

    def create_default_configuration(self, **kwargs) -> None:
        pass

    def create_configuration(self, config_file_path: str) -> None:
        self.load_configuration_yaml(config_file_path)

    def load_configuration(self) -> None:
        pass
