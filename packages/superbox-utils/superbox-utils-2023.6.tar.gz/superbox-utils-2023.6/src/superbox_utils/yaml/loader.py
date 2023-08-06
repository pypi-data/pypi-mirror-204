import yaml  # type: ignore
from pathlib import Path
from superbox_utils.config.exception import ConfigException
from typing import Union


def yaml_loader_safe(yaml_file: Path) -> Union[dict, list]:
    """Read a YAML file.

    Parameters
    ----------
    yaml_file: Path
        Path to the YAML file.

    Returns
    -------
    YAML file content as dict or list

    Raises
    ------
    ConfigException
        Raise if the YAML file can't be read.
    """
    try:
        return yaml.load(yaml_file.read_text(), Loader=yaml.FullLoader)
    except yaml.MarkedYAMLError as error:
        raise ConfigException(f"Can't read YAML file!\n{str(error.problem_mark)}") from error
