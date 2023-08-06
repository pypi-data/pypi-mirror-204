from dataclasses import dataclass
from typing import Optional, List
from typing_extensions import Literal

from .annotations import Annotation
from .sensors import Sensor
from .annotations.attributes import AttributePath

@dataclass
class Scene:
    sensors: Optional[List[Sensor]] = None
    annotations: Optional[List[Annotation]] = None
    attributes: Optional[List[AttributePath]] = None
    time_offset: Optional[int] = None
    time_unit: Optional[
        Literal["milliseconds", "microseconds", "nanoseconds"]
    ] = "microseconds"

    def add_sensor(self) -> None:
        pass

