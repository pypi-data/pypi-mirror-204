from .common import AnnotationID, SensorID, AnnotationKind
from dataclasses import dataclass
from typing import List, Union, Optional, Literal

# Define AttributePath dataclass
@dataclass
class AttributePath:
    name: str
    timestamps: List[int]
    values: List[Union[str, int, List[str]]]
    sensor_id: Optional[SensorID] = None
    static: bool = False

# Define AttributesAnnotation dataclass
@dataclass
class AttributesAnnotation:
    id: AnnotationID
    type: Literal[AnnotationKind.Attributes] = AnnotationKind.Attributes
    parent_id: Optional[AnnotationID] = None
    attributes: Optional[List[AttributePath]] = None
    sensor_attributes: Optional[List[AttributePath]] = None

