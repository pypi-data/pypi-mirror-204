from .channel import Channel
from .const import ChannelMode, ChannelType, ReadOnlyClass


class CoEChannel(Channel, metaclass=ReadOnlyClass):
    """Class to display an digital or analog datapoint."""

    def __init__(self, mode: ChannelMode, index: int, value: float, unit: str) -> None:
        """Initialize and parse json to get properties."""
        self.type = mode
        self.index = index
        self.value = value
        self.unit = unit

        super().__init__()
