from typing import Any, Dict

from . import Channel
from .const import ChannelMode, ChannelType, ReadOnlyClass


class CMIChannel(Channel, metaclass=ReadOnlyClass):
    """Class to display an input or output."""

    def __init__(self, mode: ChannelType, json: Dict[str, Any]) -> None:
        """Initialize and parse json to get properties."""
        super().__init__()
        self.mode: ChannelType = mode
        self.type: ChannelMode = json["AD"]
        self.index: int = json["Number"]
        self.value: float = json["Value"]["Value"]
        self.unit: str = json["Value"]["Unit"]
