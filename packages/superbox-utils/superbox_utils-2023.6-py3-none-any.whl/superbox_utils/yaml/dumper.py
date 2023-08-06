import yaml  # type: ignore
from yaml import Loader


class Dumper(yaml.Dumper):  # pylint: disable=too-many-ancestors
    """Custom dumper for correct indentation."""

    def increase_indent(self, flow=False, indentless=False):
        """Disable indentless."""
        return super().increase_indent(flow, False)


def yaml_dumper(content: str) -> str:
    """Convert a JSON string into a YAML string.

    Parameters
    ----------
    content: str
        JSON content as string

    Returns
    -------
    str:
        YAML content as string
    """
    return yaml.dump(
        yaml.load(content, Loader=Loader),
        Dumper=Dumper,
        default_flow_style=False,
    )
