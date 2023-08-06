from dependency_injector import providers
import json
import os
from tarvis.common import environ
from tarvis.common.environ import PlatformType, DeploymentType


class Configuration(providers.Configuration):
    def __init__(self, path: str = ".") -> None:
        super().__init__()
        self._load_environmental_configs(path)

    def _load_environment_config(
        self,
        path: str,
        platform: PlatformType | None,
        deployment: DeploymentType | None,
    ) -> None:
        file_name = "config"
        if platform is not None:
            file_name += "-" + PlatformType(platform).name.lower()
        if deployment is not None:
            file_name += "-" + DeploymentType(deployment).name.lower()
        file_name += ".json"
        file_name = os.path.join(path, file_name)
        if os.path.isfile(file_name):
            with open(file_name) as json_file:
                self.from_dict(json.load(json_file))

    def _load_environmental_configs(self, path: str) -> None:
        self._load_environment_config(path, None, None)
        self._load_environment_config(path, environ.platform, None)
        self._load_environment_config(path, None, environ.deployment)
        self._load_environment_config(path, environ.platform, environ.deployment)
