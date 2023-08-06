
@dataclass
class EventAnnotation:
    id: AnnotationID
    start: int
    type: Literal["event"] = "event"
    parent_id: Optional[AnnotationID] = None
    label: Optional[str] = None
    attributes: Optional[List[AttributePath]] = None
    duration: Optional[int] = None
    sensor_id: Optional[SensorID] = None
